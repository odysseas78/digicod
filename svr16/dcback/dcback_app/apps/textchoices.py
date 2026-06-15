from django.db import models


class SupplierCode(models.TextChoices):
    PREPAIDFORGE = "PREPAIDFORGE", "Prepaidforge"

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