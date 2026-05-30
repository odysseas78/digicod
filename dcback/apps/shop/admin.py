from django.contrib import admin

from .models import *
# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    # list_display = ('user__username', 'user__first_name', 'user__last_name')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
admin.site.register(Customer, CustomerAdmin)

# admin.site.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # list_display = ('user__username', 'user__first_name', 'user__last_name')
    search_fields = ['title', 'id']
admin.site.register(Product, ProductAdmin)

class BrandAdmin(admin.ModelAdmin):
    # list_display = ('user__username', 'user__first_name', 'user__last_name')
    search_fields = ['title', 'id']
admin.site.register(Brand, BrandAdmin)

admin.site.register(Category)



class CartAdmin(admin.ModelAdmin):
    list_display = ['id']
admin.site.register(Cart, CartAdmin)



admin.site.register(CartProduct)

# class OrderAdmin(admin.ModelAdmin):
#     # list_display = ('user__username', 'user__first_name', 'user__last_name')
#     search_fields = ['id', 'customer__user__username', 'customer__user__email']
# admin.site.register(Order, OrderAdmin)



admin.site.register(Payment)
admin.site.register(Currency)

# class WalletAdmin(admin.ModelAdmin):
#     # list_display = ('user__username', 'user__first_name', 'user__last_name')
#     search_fields = ['owner__user__username', 'owner__user__id', 'description']
# admin.site.register(Wallet, WalletAdmin)

# admin.site.register(CoinWallet)
# admin.site.register(CoinWalletTransaction)
# admin.site.register(CoinWalletDeposit)
# admin.site.register(CoinWalletSegment)
admin.site.register(Limit)
# admin.site.register(WalletOrder)
admin.site.register(ProductCode)
# admin.site.register(ProductCodes)

# admin.site.register(CryptoAddress)
# admin.site.register(CryptoNetwork)
# admin.site.register(PaymentCallback)
admin.site.register(Payoptions)
# admin.site.register(Verification)
# admin.site.register(File)
# admin.site.register(Jsonfile)
# admin.site.register(Message)
# admin.site.register(Polzov)
# admin.site.register(UrlToken)
class PriceRabattAdmin(admin.ModelAdmin):
    # list_display = ('user__username', 'user__first_name', 'user__last_name')
    search_fields = ['customer__user__username', 'brand__title', 'product__title']
    autocomplete_fields = ['customer', 'brand', 'product']
# admin.site.register(PriceRabatt, PriceRabattAdmin)

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ("name", "parent")
#     search_fields = ("name",)


# @admin.register(Brand)
# class BrandAdmin(admin.ModelAdmin):
#     list_display = ("name",)
#     search_fields = ("name",)


# @admin.register(Partner)
# class PartnerAdmin(admin.ModelAdmin):
#     list_display = ("name", "code", "is_active")
#     search_fields = ("name", "code")


# @admin.register(PartnerApiToken)
# class PartnerApiTokenAdmin(admin.ModelAdmin):
#     list_display = ("partner", "valid_until", "updated_at")


# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ("name", "brand", "category", "face_value_amount", "face_value_currency", "is_active")
#     list_filter = ("brand", "category", "is_active")
#     search_fields = ("name", "slug")


# @admin.register(PartnerProduct)
# class PartnerProductAdmin(admin.ModelAdmin):
#     list_display = ("sku", "product", "partner", "retail_price", "cost_price", "available_stock", "is_active")
#     list_filter = ("partner", "delivery_type", "product_type", "is_active")
#     search_fields = ("sku", "external_id", "product__name")


# class CartItemInline(admin.TabularInline):
#     model = CartItem
#     extra = 0


# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ("id", "customer", "session_key", "created_at")
#     inlines = [CartItemInline]


# @admin.register(CustomerProfile)
# class CustomerProfileAdmin(admin.ModelAdmin):
#     list_display = ("user", "account_type", "created_at")
#     list_filter = ("account_type",)
#     search_fields = ("user__email", "user__username", "user__first_name", "user__last_name")


# class DeliveredCodeInline(admin.TabularInline):
#     model = DeliveredCode
#     extra = 0


# class CustomerOrderItemInline(admin.TabularInline):
#     model = CustomerOrderItem
#     extra = 0


# @admin.register(CustomerOrder)
# class CustomerOrderAdmin(admin.ModelAdmin):
#     list_display = ("number", "customer", "status", "total_amount", "created_at")
#     list_filter = ("status", "currency")
#     search_fields = ("number", "customer__user__email")
#     inlines = [CustomerOrderItemInline]


# @admin.register(CustomerOrderItem)
# class CustomerOrderItemAdmin(admin.ModelAdmin):
#     list_display = ("order", "product_name", "product_sku", "quantity", "unit_price")
#     search_fields = ("order__number", "product_name", "product_sku", "fulfillment_reference")
#     inlines = [DeliveredCodeInline]


# @admin.register(SupplierOrder)
# class SupplierOrderAdmin(admin.ModelAdmin):
#     list_display = ("partner", "custom_order_reference", "supplier_order_reference", "sku", "status")
#     list_filter = ("partner", "status", "delivery_type")
#     search_fields = ("custom_order_reference", "supplier_order_reference", "sku")
