from django.urls import path, re_path
from eshop.views import TestView, WalletViewSet, WalletOrderView, ProductCodeView
from rest_framework.routers import SimpleRouter

from .views import ProductViewSet, CategoryViewSet, CurrentUserView, UserAPIView, BrandViewSet, RegisterView, \
    LogoutView, LogoutAllView, OrderViewSet, PaymentView, CurrencyView, VerifView, OtherView, LoginView
from ..adminka.views import OrdersViewSet, CustomersViewSet, UsersViewSet, WalletOrdersView, \
    ProductsView, BrandsView, LimitsView, AdminAPI
from ..cart.views import CartViewSet
from eshop.payment.views import *

main_router = SimpleRouter()

main_router.register('product', ProductViewSet, basename='product')
main_router.register('category', CategoryViewSet, basename='category')
main_router.register('brand', BrandViewSet, basename='brand')
main_router.register('cart', CartViewSet, basename='cart')
main_router.register('order', OrderViewSet, basename='order')
main_router.register('orders', OrdersViewSet, basename='orders')
main_router.register('wallet', WalletViewSet, basename='wallet')
# main_router.register('wallet2', Wallet2ViewSet, basename='wallet2')
main_router.register('customers', CustomersViewSet, basename='customers')
main_router.register('users', UsersViewSet, basename='users')
main_router.register('walletorders', WalletOrdersView, basename='walletorders')
main_router.register('wallet_order', WalletOrderView, basename='walletorder')
main_router.register('admin', AdminAPI, basename='admin_api')
main_router.register('products', ProductsView, basename='products')
main_router.register('brands', BrandsView, basename='brands')
main_router.register('limits', LimitsView, basename='limits')
main_router.register('payment', PaymentView, basename='payment')
main_router.register('currency', CurrencyView, basename='currency')
main_router.register('test', TestView, basename='test')



extra_urlpatterns = [
    path('login/', LoginView.as_view(), name='auth_login'),
    path('check-user-is-authenticated/', CurrentUserView.as_view(), name='check-user-is-authenticated'),
    path('user/', UserAPIView.as_view(), name='user'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all'),
    # path('walletorders/', WalletOrdersView.as_view(), name='walletorders'),
    re_path('^walletorders/(?P<owner>.+)/$', WalletOrdersView.as_view('get'), name='walletorders'),
    # path('wallet_order/', WalletOrderView, name='wallet_order'),
    path('product_code/', ProductCodeView.as_view(), name='product_code'),
    path('verif/', VerifView.as_view(), name='verif'),
    path('other/', OtherView.as_view(), name='other'),
    path('gate/', PaymentGate.as_view(), name="gate"),

]