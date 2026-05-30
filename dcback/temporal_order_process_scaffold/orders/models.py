from __future__ import annotations

import uuid
from decimal import Decimal
from django.db import models

class SupplierCode(models.TextChoices):
    PREPAIDFORGE = "PREPAIDFORGE", "PrepaidForge", "Prepaidforge", "prepaidforge"

class ProductStockStatus(models.TextChoices):
    IN_STOCK = "IN_STOCK", "In stock"
    LOW_STOCK = "LOW_STOCK", "Low stock"
    OUT_OF_STOCK = "OUT_OF_STOCK", "Out of stock"
    UNKNOWN = "UNKNOWN", "Unknown"

class CartValidationStatus(models.TextChoices):
    OK = "OK", "OK"
    CART_CHANGED = "CART_CHANGED", "Cart changed"

class OrderStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    CART_NEEDS_CONFIRMATION = "CART_NEEDS_CONFIRMATION", "Cart needs confirmation"
    CONFIRMED = "CONFIRMED", "Confirmed"
    PAYMENT_PENDING = "PAYMENT_PENDING", "Payment pending"
    PAYMENT_AUTHORIZED = "PAYMENT_AUTHORIZED", "Payment authorized"
    PAID = "PAID", "Paid"
    FULFILLMENT_STARTED = "FULFILLMENT_STARTED", "Fulfillment started"
    SUPPLIER_PURCHASE_PENDING = "SUPPLIER_PURCHASE_PENDING", "Supplier purchase pending"
    SUPPLIER_PURCHASE_UNCERTAIN = "SUPPLIER_PURCHASE_UNCERTAIN", "Supplier purchase uncertain"
    SUPPLIER_PURCHASED = "SUPPLIER_PURCHASED", "Supplier purchased"
    CODES_STORED = "CODES_STORED", "Codes stored"
    EMAIL_PENDING = "EMAIL_PENDING", "Email pending"
    EMAIL_SENT = "EMAIL_SENT", "Email sent"
    COMPLETED = "COMPLETED", "Completed"
    FAILED_NEEDS_REVIEW = "FAILED_NEEDS_REVIEW", "Failed - needs review"
    REFUND_PENDING = "REFUND_PENDING", "Refund pending"
    REFUNDED = "REFUNDED", "Refunded"
    CANCELLED = "CANCELLED", "Cancelled"

class SupplierPurchaseStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SUCCESS = "SUCCESS", "Success"
    FAILED = "FAILED", "Failed"
    UNCERTAIN = "UNCERTAIN", "Uncertain"

class EmailDeliveryStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SENT = "SENT", "Sent"
    FAILED = "FAILED", "Failed"

class SupplierProduct(models.Model):
    supplier = models.CharField(max_length=50, choices=SupplierCode.choices)
    supplier_sku = models.CharField(max_length=255)
    name_original = models.CharField(max_length=500)
    brand = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255, blank=True)
    currency = models.CharField(max_length=3, default="EUR")
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    stock_status = models.CharField(max_length=30, choices=ProductStockStatus.choices, default=ProductStockStatus.UNKNOWN)
    stock_quantity = models.PositiveIntegerField(null=True, blank=True)
    supplier_active = models.BooleanField(default=True)
    raw_payload = models.JSONField(default=dict, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    last_price_changed_at = models.DateTimeField(null=True, blank=True)
    last_stock_changed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["supplier", "supplier_sku"], name="uniq_supplier_product")]
        indexes = [models.Index(fields=["supplier", "supplier_sku"]), models.Index(fields=["supplier_active", "stock_status"])]

    def __str__(self):
        return f"{self.supplier}:{self.supplier_sku} {self.name_original}"

class ShopProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier_product = models.ForeignKey(SupplierProduct, on_delete=models.PROTECT)
    slug = models.SlugField(max_length=255, unique=True)
    public_name = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    selling_currency = models.CharField(max_length=3, default="EUR")
    selling_price = models.DecimalField(max_digits=12, decimal_places=2)
    active_in_shop = models.BooleanField(default=True)
    max_quantity_per_order = models.PositiveIntegerField(default=10)
    raw_shop_metadata = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.public_name

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_email = models.EmailField()
    customer_user_id = models.BigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.DRAFT)
    currency = models.CharField(max_length=3, default="EUR")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    cart_token = models.CharField(max_length=100, blank=True)
    cart_confirmed_at = models.DateTimeField(null=True, blank=True)
    payment_reference = models.CharField(max_length=255, blank=True)
    payment_status = models.CharField(max_length=50, blank=True)
    temporal_workflow_id = models.CharField(max_length=255, blank=True)
    failure_reason = models.TextField(blank=True)
    admin_note = models.TextField(blank=True)
    order_snapshot = models.JSONField(default=dict, blank=True)
    last_error_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["status"]), models.Index(fields=["customer_email"]), models.Index(fields=["temporal_workflow_id"])]

    def __str__(self):
        return f"{self.id} {self.customer_email} {self.status}"

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    shop_product = models.ForeignKey(ShopProduct, on_delete=models.PROTECT)
    supplier_product = models.ForeignKey(SupplierProduct, on_delete=models.PROTECT)
    product_name_snapshot = models.CharField(max_length=500)
    supplier_sku_snapshot = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)
    supplier_purchase_price_snapshot = models.DecimalField(max_digits=12, decimal_places=2)
    raw_snapshot = models.JSONField(default=dict, blank=True)

class SupplierPurchase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name="supplier_purchases", on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, related_name="supplier_purchases", on_delete=models.CASCADE)
    supplier = models.CharField(max_length=50, choices=SupplierCode.choices)
    supplier_sku = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    idempotency_key = models.CharField(max_length=255, unique=True)
    supplier_order_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=50, choices=SupplierPurchaseStatus.choices, default=SupplierPurchaseStatus.PENDING)
    request_payload = models.JSONField(default=dict, blank=True)
    response_payload = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    uncertain_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    succeeded_at = models.DateTimeField(null=True, blank=True)

class PurchasedCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name="purchased_codes", on_delete=models.CASCADE)
    order_item = models.ForeignKey(OrderItem, related_name="purchased_codes", on_delete=models.CASCADE)
    supplier_purchase = models.ForeignKey(SupplierPurchase, related_name="codes", on_delete=models.CASCADE)
    code_encrypted = models.TextField()
    pin_encrypted = models.TextField(blank=True)
    serial_number_encrypted = models.TextField(blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    email_message_id = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class EmailDelivery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, related_name="email_deliveries", on_delete=models.CASCADE)
    recipient = models.EmailField()
    template = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=EmailDeliveryStatus.choices, default=EmailDeliveryStatus.PENDING)
    provider_message_id = models.CharField(max_length=255, blank=True)
    attempts = models.PositiveIntegerField(default=0)
    last_error = models.TextField(blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderEvent(models.Model):
    order = models.ForeignKey(Order, related_name="events", on_delete=models.CASCADE)
    type = models.CharField(max_length=100)
    message = models.TextField(blank=True)
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

def add_order_event(order: Order, type_: str, message: str = "", payload: dict | None = None) -> None:
    OrderEvent.objects.create(order=order, type=type_, message=message, payload=payload or {})
