from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin

import requests
from django.conf import settings

from apps.shop.models import Supplier, Datafile
from apps.shop.services import PrepaidForgeError, sync_products_from_supplier


class PrepaidForgeClient:
    def __init__(self):
        self.supplier = Supplier.objects.filter(name='Prepaidforge').first()
        if self.supplier is None:
            raise PrepaidForgeError("PrepaidForge supplier is missing.")
        self.jdata = self.supplier.extra_data or {}
        self.base_url = 'https://api.prepaidforge.com/v1/1.0/'
        self.sign_in_url = 'https://api.prepaidforge.com/v1/1.0/signInWithApi'
        self.katalog_url = 'https://api.prepaidforge.com/v1/1.0/findAllProducts'
        self.find_stocks_url = f'https://api.prepaidforge.com/v1/1.0/findStocks'
        self.create_api_order_url = 'https://api.prepaidforge.com/v1/1.0/createApiOrder'
        # self.partner = get_or_create_partner("prepaidforge", "PrepaidForge", self.base_url)

    def _request(self, method, path, headers=None, **kwargs):
        response = requests.request(
            method=method,
            url=urljoin(f"{self.base_url}/", path.lstrip("/")),
            headers={"Content-Type": "application/json", **(headers or {})},
            # timeout=self.timeout,
            **kwargs,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise PrepaidForgeError(f"PrepaidForge request failed: {response.text}") from exc
        if not response.content:
            return {}
        return response.json()

    def _credentials(self):
        shop_settings = Datafile.objects.filter(name="Shopsettings").first()
        testmode = bool(
            shop_settings
            and isinstance(shop_settings.jdata, dict)
            and shop_settings.jdata.get("testmode")
        )
        if testmode:
            return (
                getattr(settings.ENV_DICT, "TEST_PF_EMAIL", None),
                getattr(settings.ENV_DICT, "TEST_PF_PASSWORD", None),
            )
        return (
            getattr(settings.ENV_DICT, "PF_EMAIL", None),
            getattr(settings.ENV_DICT, "PF_PASSWORD", None),
        )

    def sign_in(self):
        email, password = self._credentials()
        if not email or not password:
            raise PrepaidForgeError("PrepaidForge credentials are missing.")

        payload = self._request(
            "POST",
            self.sign_in_url,
            json={
                "email": email,
                "password": password,
            },
        )
        token = payload.get("apiToken")
        if not token:
            raise PrepaidForgeError("PrepaidForge did not return an apiToken.")

        valid_until_raw = payload.get("tokenValidUntil")
        if valid_until_raw:
            valid_until = datetime.fromtimestamp(int(valid_until_raw) / 1000, tz=timezone.utc)
        else:
            valid_until = datetime.now(tz=timezone.utc) + timedelta(hours=1)

        self.jdata['apiToken'] = {"token": token, "valid_until": valid_until.isoformat()}
        return token

    def _parse_valid_until(self, value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return None
        return None

    def get_api_token(self):
        token_obj = self.jdata.get('apiToken')
        now = datetime.now(tz=timezone.utc)
        valid_until = self._parse_valid_until(token_obj.get("valid_until")) if token_obj else None
        if valid_until and valid_until > now + timedelta(minutes=1):
            return token_obj.get('token')
        return self.sign_in()

    def find_all_products(self):
        return self._request("GET", self.katalog_url)

    def find_stocks(self, skus):
        data = {"types": ["TEXT", "SCAN"], "skus": [*skus]}
        token = self.get_api_token()
        return self._request(
            "POST",
            self.find_stocks_url,
             json=data,
            headers={"X-PrepaidForge-Api-Token": token},
        )

    def deduplicate_products(self, items):
        """
        Entfernt doppelte Produkte.
        Pro product bleibt das Objekt mit der höchsten quantity.
        """

        unique = {}

        for item in items:
            product = item["product"]

            if product not in unique:
                unique[product] = item
                continue

            if item["purchasePrice"] > unique[product]["purchasePrice"]:
                unique[product] = item

        return list(unique.values())
    
    def sync_products(self):
        catalog_payload = self.find_all_products()
        products = catalog_payload.get("results") if isinstance(catalog_payload, dict) else catalog_payload
        if not isinstance(products, list):
            raise PrepaidForgeError("Catalog response is not a list.")

        skus = {
            product.get("sku")
            for product in products
            if isinstance(product, dict) and product.get("sku")
        }
        stock_payload = self.find_stocks(list(skus))
        stock_items = stock_payload.get("results") if isinstance(stock_payload, dict) else stock_payload
        if not isinstance(stock_items, list):
            raise PrepaidForgeError("Stock response is not a list.")

        stocks = self.deduplicate_products(stock_items)
        sync_products_from_supplier(stocks, products, self.supplier)
        return {
            "ok": True,
            "products": len(products),
            "stocks": len(stocks),
            "skus": len(skus),
        }
        # stock_index = {str(item.get("product") or item.get("sku")): item for item in stocks if item.get("product") or item.get("sku")}
        # synced = []
        # for stock in stocks:
        #     filtrprod = [product for product in products if product.get("sku") == stock.get("product")]
        #     product = filtrprod if isinstance(filtrprod, dict) else filtrprod[0]
        #     # filtrstock = [stock for stock in stocks if stock.get("product") == stock.get("product")]
        #     # stock = filtrstock if isinstance(filtrstock, dict) else filtrstock[0]
        #     product_payload = {"product":product, "stock":stock}
        #     if product_payload:
        #         synced.append(sync_product_from_supplier(product_payload, sku))
        # return synced

    def find_stock_for_sku(self, sku):
        stock_payload = self.find_stocks()
        stocks = stock_payload.get("results") if isinstance(stock_payload, dict) else stock_payload
        for item in stocks:
            if str(item.get("product") or item.get("sku")) == sku:
                return item
        raise PrepaidForgeError(f"No stock information found for sku {sku}.")

    def create_api_order(self, sku, price, code_type, custom_order_reference):
        token = self.get_api_token()
        payload = self._request(
            "POST",
            settings.PREPAIDFORGE_PURCHASE_PATH,
            headers={"X-PrepaidForge-Api-Token": token},
            json={
                "sku": sku,
                "price": float(price),
                "codeType": code_type,
                "customOrderReference": custom_order_reference,
            },
        )
        # SupplierOrder.objects.update_or_create(
        #     partner=self.partner,
        #     custom_order_reference=custom_order_reference,
        #     defaults={
        #         "supplier_order_reference": str(payload.get("orderReference") or ""),
        #         "sku": sku,
        #         "requested_price": normalize_money(price),
        #         "delivery_type": payload.get("codeType") or code_type,
        #         "status": SupplierOrder.Status.COMPLETED,
        #         "raw_payload": payload,
        #         "failure_reason": "",
        #     },
        # )
        return payload
