from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Brand, Cart, Category, CustomerOrder, CustomerProfile, Partner, PartnerProduct, Product
from .services import upsert_partner_product_from_supplier


class ShopApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Giftcards", slug="giftcards")
        self.brand = Brand.objects.create(name="Amazon", slug="amazon")
        self.partner = Partner.objects.create(name="PrepaidForge", code="prepaidforge")
        self.product = Product.objects.create(
            name="Amazon Gift Card 10 USD",
            slug="amazon-gift-card-10-usd",
            brand=self.brand,
            category=self.category,
            face_value_amount="10.0000",
            face_value_currency="USD",
        )
        self.offer = PartnerProduct.objects.create(
            partner=self.partner,
            product=self.product,
            external_id="Amazon-10-USD",
            sku="Amazon-10-USD",
            currency="USD",
            retail_price="10.0000",
            cost_price="9.5000",
            available_stock=5,
            delivery_type="TEXT",
            product_type="GIFTCARD",
        )

    def test_product_list(self):
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["sku"], "Amazon-10-USD")
        self.assertEqual(response.data[0]["brand"]["name"], "Amazon")

    def test_add_to_cart(self):
        response = self.client.post("/api/cart/items/", {"partner_product_id": self.offer.id, "quantity": 2}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["items"][0]["quantity"], 2)
        self.assertEqual(Cart.objects.count(), 1)

    @patch("apps.shop.views.process_order_task.delay")
    def test_checkout_creates_guest_customer_and_order(self, delay_mock):
        self.client.post("/api/cart/items/", {"partner_product_id": self.offer.id, "quantity": 1}, format="json")

        response = self.client.post(
            "/api/checkout/",
            {
                "email": "max@example.com",
                "first_name": "Max",
                "last_name": "Mustermann",
                "create_account": False,
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CustomerOrder.objects.count(), 1)
        self.assertEqual(CustomerProfile.objects.first().account_type, CustomerProfile.AccountType.GUEST)
        delay_mock.assert_called_once()

    @patch("apps.shop.views.process_order_task.delay")
    def test_checkout_creates_registered_customer(self, delay_mock):
        self.client.post("/api/cart/items/", {"partner_product_id": self.offer.id, "quantity": 1}, format="json")

        response = self.client.post(
            "/api/checkout/",
            {
                "email": "anna@example.com",
                "first_name": "Anna",
                "last_name": "Muster",
                "create_account": True,
                "password": "VerySafePass123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(email="anna@example.com")
        self.assertTrue(user.has_usable_password())
        self.assertEqual(user.customer_profile.account_type, CustomerProfile.AccountType.REGISTERED)
        delay_mock.assert_called_once()

    def test_upsert_product_from_realistic_supplier_payload(self):
        offer = upsert_partner_product_from_supplier(
            self.partner,
            {
                "sku": "Zalando-25-EUR-DE",
                "name": "Zalando 25 EUR DE",
                "faceValue": {"amount": 25.0, "currency": "EUR"},
                "defaultPrice": {"amount": 0.0, "currency": "EUR"},
                "currencyCode": "EUR",
                "imageUrl": "https://example.com/item.png",
                "active": True,
                "languages": [],
                "countries": ["de"],
                "platforms": [],
                "productType": "GIFTCARD",
                "category": ["Giftcards"],
                "brand": "Zalando",
            },
            {
                "product": "Zalando-25-EUR-DE",
                "type": "TEXT",
                "quantity": 2101,
                "purchasePrice": 23.675,
            },
        )
        self.assertEqual(offer.sku, "Zalando-25-EUR-DE")
        self.assertEqual(offer.product.brand.name, "Zalando")
        self.assertEqual(offer.product.category.name, "Giftcards")
        self.assertEqual(offer.available_stock, 2101)
        self.assertEqual(str(offer.cost_price), "23.6750")
        self.assertEqual(str(offer.retail_price), "25.0000")
        self.assertEqual(offer.delivery_type, "TEXT")
