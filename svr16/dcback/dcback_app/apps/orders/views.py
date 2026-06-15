from __future__ import annotations

from asgiref.sync import async_to_sync
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from orders.models import Order, OrderStatus
from orders.services.cart_validation import validate_cart, create_order_from_validated_cart
from orders.services.order_service import start_order_fulfillment

class ValidateCartAPIView(APIView):
    def post(self, request):
        return Response(validate_cart(request.data.get("items", [])))

class ConfirmOrderAPIView(APIView):
    def post(self, request):
        validated_cart = validate_cart(request.data.get("items", []))
        if validated_cart["status"] != "OK":
            return Response(validated_cart, status=status.HTTP_409_CONFLICT)
        order = create_order_from_validated_cart(
            customer_email=request.data["customer_email"],
            customer_user_id=getattr(request.user, "id", None) if request.user.is_authenticated else None,
            validated_cart=validated_cart,
        )
        return Response({"order_id": str(order.id), "status": order.status, "total": str(order.total), "currency": order.currency}, status=status.HTTP_201_CREATED)

class StartFulfillmentDebugAPIView(APIView):
    def post(self, request, order_id: str):
        order = Order.objects.get(id=order_id)
        order.status = OrderStatus.PAYMENT_AUTHORIZED
        order.payment_status = "AUTHORIZED_DEBUG"
        order.save(update_fields=["status", "payment_status", "updated_at"])
        workflow_id = async_to_sync(start_order_fulfillment)(str(order.id))
        return Response({"workflow_id": workflow_id, "order_id": str(order.id)})

class OrderStatusAPIView(APIView):
    def get(self, request, order_id: str):
        order = Order.objects.get(id=order_id)
        return Response({"order_id": str(order.id), "status": order.status, "total": str(order.total), "currency": order.currency, "failure_reason": order.failure_reason, "completed_at": order.completed_at})
