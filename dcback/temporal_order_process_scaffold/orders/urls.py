from django.urls import path
from .views import ValidateCartAPIView, ConfirmOrderAPIView, StartFulfillmentDebugAPIView, OrderStatusAPIView

urlpatterns = [
    path("checkout/validate-cart/", ValidateCartAPIView.as_view()),
    path("checkout/confirm/", ConfirmOrderAPIView.as_view()),
    path("orders/<uuid:order_id>/status/", OrderStatusAPIView.as_view()),
    path("orders/<uuid:order_id>/debug-start-fulfillment/", StartFulfillmentDebugAPIView.as_view()),
]
