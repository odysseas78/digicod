from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.shop.views import (
    BrandView,
    CartViewSet,
    CategoryView,
    CurrencyView,
    PaymentView,
    ProductView
)


# main_router = SimpleRouter()

# main_router.register('cart', CartViewSet, basename='cart')

urlpatterns = [
   
    # path("product/", ProductView.as_view(), name="product"),
    # path("brand/", BrandView.as_view(), name="brand"),
    # path("category/", CategoryView.as_view(), name="category"),
    # path("currency/", CurrencyView.as_view(), name="currency"),
    # path("payment/", PaymentView.as_view(), name="payment"),
]

# urlpatterns += main_router.urls
