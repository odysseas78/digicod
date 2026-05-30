from django.urls import path, re_path
from rest_framework.routers import SimpleRouter
from eshop_api.adminka.views import Orders2ViewSet, admin_index, OrdersViewSet, ActionSViewSet, \
    WordersViewSet, CustomersViewSet, LoginstatViewSet, Brands2ViewSet, Product2ViewSet, \
        CartsViewSet, CartProductViewSet, WalletViewSet, CategoriesViewSet

#
admin_router = SimpleRouter()
#
admin_router.register('orders2', Orders2ViewSet, basename='orders2')
admin_router.register('worders2', WordersViewSet, basename='worders2')
admin_router.register('customers', CustomersViewSet, basename='customers')
admin_router.register('loginstat', LoginstatViewSet, basename='loginstat')
admin_router.register('actions', ActionSViewSet, basename='actionsviewset')
admin_router.register('brands2', Brands2ViewSet, basename='brand2')
admin_router.register('product2', Product2ViewSet, basename='product2')
admin_router.register('carts', CartsViewSet, basename='carts')
admin_router.register('cart_product', CartProductViewSet, basename='cart_product')
admin_router.register('wallet2', WalletViewSet, basename='wallet')
admin_router.register('categories', CategoriesViewSet, basename='categories')


# main_router.register('cart', CartViewSet, basename='cart')
# main_router.register('order', OrderViewSet, basename='order')
# main_router.register('wallet', WalletViewSet, basename='wallet')


urlpatterns = [
    path('admin_index/', admin_index),
    path('orders/<pk>/', OrdersViewSet.as_view({'get':'list', 'post': 'create', 'delete':'destroy' }),
         name='orders'),
    # path('actionview', ActionSView.as_view({'get':'get'}), name='actionviewset'),
]