from django.contrib import admin
# from .models import SupplierProduct, ShopProduct, Order, OrderItem, SupplierPurchase, PurchasedCode, EmailDelivery, OrderEvent

# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0

# class SupplierPurchaseInline(admin.TabularInline):
#     model = SupplierPurchase
#     extra = 0
#     readonly_fields = ["id", "idempotency_key", "supplier_order_id", "status", "error_message"]

# class EmailDeliveryInline(admin.TabularInline):
#     model = EmailDelivery
#     extra = 0
#     readonly_fields = ["id", "status", "attempts", "last_error", "sent_at"]

# class OrderEventInline(admin.TabularInline):
#     model = OrderEvent
#     extra = 0
#     readonly_fields = ["type", "message", "payload", "created_at"]

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ["id", "customer_email", "status", "total", "currency", "created_at", "completed_at"]
#     list_filter = ["status", "currency", "created_at"]
#     search_fields = ["id", "customer_email", "temporal_workflow_id", "payment_reference"]
#     readonly_fields = ["id", "temporal_workflow_id", "order_snapshot", "last_error_payload", "created_at", "updated_at"]
#     inlines = [OrderItemInline, SupplierPurchaseInline, EmailDeliveryInline, OrderEventInline]

# admin.site.register(SupplierProduct)
# admin.site.register(ShopProduct)
# admin.site.register(PurchasedCode)
