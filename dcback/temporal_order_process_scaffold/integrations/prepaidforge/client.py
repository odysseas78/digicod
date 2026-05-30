from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any
import httpx
from django.conf import settings

class PrepaidForgeError(Exception): ...
class PrepaidForgeUnavailableError(PrepaidForgeError): ...

class PrepaidForgePurchaseUncertainError(PrepaidForgeError):
    """
    Request may have reached supplier, but response was lost.
    Do not blindly retry purchases after this.
    """

@dataclass(frozen=True)
class PrepaidForgeProduct:
    sku: str
    name: str
    brand: str
    category: str
    currency: str
    purchase_price: Decimal
    stock_status: str
    stock_quantity: int | None
    active: bool
    raw: dict[str, Any]

@dataclass(frozen=True)
class PrepaidForgeCode:
    code: str
    pin: str = ""
    serial_number: str = ""
    expires_at: str | None = None

@dataclass(frozen=True)
class PrepaidForgePurchaseResult:
    supplier_order_id: str
    codes: list[PrepaidForgeCode]
    raw: dict[str, Any]

class PrepaidForgeClient:
    """
    TODO: Replace endpoint paths and field mapping with exact PrepaidForge docs.
    Keep purchase calls without internal retries. Temporal controls retries.
    """

    def __init__(self) -> None:
        self.base_url = settings.PREPAIDFORGE_BASE_URL.rstrip("/")
        self.api_key = settings.PREPAIDFORGE_API_KEY
        self.sandbox = bool(getattr(settings, "PREPAIDFORGE_SANDBOX", False))

    def _headers(self, idempotency_key: str | None = None) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",  # TODO adjust if needed
        }
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return headers
   
    async def list_products(self) -> list[PrepaidForgeProduct]:
        url = f"{self.base_url}/products"  # TODO
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.get(url, headers=self._headers())
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise PrepaidForgeUnavailableError(str(exc)) from exc

        data = response.json()
        rows = data.get("products", data if isinstance(data, list) else [])
        return [
            PrepaidForgeProduct(
                sku=str(row.get("sku") or row.get("id") or row.get("product_id")),
                name=str(row.get("name") or row.get("title") or ""),
                brand=str(row.get("brand") or ""),
                category=str(row.get("category") or ""),
                currency=str(row.get("currency") or "EUR"),
                purchase_price=Decimal(str(row.get("price") or row.get("purchase_price") or "0.00")),
                stock_status=str(row.get("stock_status") or ("IN_STOCK" if row.get("available", True) else "OUT_OF_STOCK")),
                stock_quantity=row.get("stock_quantity"),
                active=bool(row.get("active", row.get("available", True))),
                raw=row,
            )
            for row in rows
        ]

    async def purchase_product(self, *, sku: str, quantity: int, client_reference: str, idempotency_key: str) -> PrepaidForgePurchaseResult:
        url = f"{self.base_url}/orders"  # TODO
        payload = {
            "product_id": sku,
            "quantity": quantity,
            "client_reference": client_reference,
            "sandbox": self.sandbox,
        }

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(url, json=payload, headers=self._headers(idempotency_key=idempotency_key))
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            raise PrepaidForgePurchaseUncertainError(str(exc)) from exc
        except httpx.HTTPError as exc:
            raise PrepaidForgeUnavailableError(str(exc)) from exc

        if response.status_code >= 500:
            raise PrepaidForgePurchaseUncertainError(f"Supplier returned {response.status_code}: {response.text[:500]}")
        if response.status_code >= 400:
            raise PrepaidForgeError(f"Supplier returned {response.status_code}: {response.text[:1000]}")

        data = response.json()
        supplier_order_id = str(data.get("order_id") or data.get("id") or data.get("supplier_order_id") or client_reference)
        raw_codes = data.get("codes") or data.get("items") or []
        codes = [
            PrepaidForgeCode(
                code=str(item.get("code") or item.get("value") or ""),
                pin=str(item.get("pin") or ""),
                serial_number=str(item.get("serial_number") or item.get("serial") or ""),
                expires_at=item.get("expires_at"),
            )
            for item in raw_codes
        ]

        if not codes:
            raise PrepaidForgeError("Supplier purchase succeeded but no codes were returned")

        return PrepaidForgePurchaseResult(supplier_order_id=supplier_order_id, codes=codes, raw=data)
