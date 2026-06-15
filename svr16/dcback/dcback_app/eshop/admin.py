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

class BasketAdmin(admin.ModelAdmin):
    list_display = ['id']
admin.site.register(Basket, BasketAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['id']
admin.site.register(Cart, CartAdmin)

class CustomTokenAdmin(admin.ModelAdmin):
    list_display = ['fingeprint', 'key', 'json', 'user', 'created_at', 'updated_at']
admin.site.register(CustomToken, CustomTokenAdmin)

admin.site.register(CartProduct)

class OrderAdmin(admin.ModelAdmin):
    # list_display = ('user__username', 'user__first_name', 'user__last_name')
    search_fields = ['id', 'customer__user__username', 'customer__user__email']
admin.site.register(Order, OrderAdmin)

class OrdersAdmin(admin.ModelAdmin):
    # fields = ['comment']
    list_display = ['id', 'basket', 'subtotal', 'total', 'status']
    search_fields = ['id', 'basket__owner__user__username']
admin.site.register(Orders, OrdersAdmin)

admin.site.register(Payment)
admin.site.register(ShopSetting)
admin.site.register(Currency)

class WalletAdmin(admin.ModelAdmin):
    # list_display = ('user__username', 'user__first_name', 'user__last_name')
    search_fields = ['owner__user__username', 'owner__user__id', 'description']
admin.site.register(Wallet, WalletAdmin)

admin.site.register(CoinWallet)
admin.site.register(CoinWalletTransaction)
admin.site.register(CoinWalletDeposit)
admin.site.register(CoinWalletSegment)
admin.site.register(Limit)
admin.site.register(WalletOrder)
admin.site.register(ProductCode)
admin.site.register(ProductCodes)

# admin.site.register(CryptoAddress)
# admin.site.register(CryptoNetwork)
admin.site.register(PaymentCallback)
admin.site.register(Payoptions)
admin.site.register(Verification)
admin.site.register(File)
admin.site.register(Jsonfile)
admin.site.register(Message)
admin.site.register(Polzov)
admin.site.register(UrlToken)
class PriceRabattAdmin(admin.ModelAdmin):
    # list_display = ('user__username', 'user__first_name', 'user__last_name')
    search_fields = ['customer__user__username', 'brand__title', 'product__title']
    autocomplete_fields = ['customer', 'brand', 'product']
admin.site.register(PriceRabatt, PriceRabattAdmin)
