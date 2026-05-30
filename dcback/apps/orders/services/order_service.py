from __future__ import annotations

from django.conf import settings
from temporalio.client import Client, WorkflowAlreadyStartedError
from orders.models import Order, OrderStatus, add_order_event
from workflows.order_fulfillment import OrderFulfillmentWorkflow

async def start_order_fulfillment(order_id: str) -> str:
    order = Order.objects.get(id=order_id)
    workflow_id = f"order-{order.id}-fulfillment"
    client = await Client.connect(settings.TEMPORAL_ADDRESS)

    try:
        handle = await client.start_workflow(
            OrderFulfillmentWorkflow.run,
            str(order.id),
            id=workflow_id,
            task_queue=settings.TEMPORAL_TASK_QUEUE_ORDER,
        )
    except WorkflowAlreadyStartedError:
        handle = client.get_workflow_handle(workflow_id)

    order.temporal_workflow_id = workflow_id
    if order.status in [OrderStatus.CONFIRMED, OrderStatus.PAYMENT_AUTHORIZED, OrderStatus.PAID]:
        order.status = OrderStatus.FULFILLMENT_STARTED
    order.save(update_fields=["temporal_workflow_id", "status", "updated_at"])
    add_order_event(order, "WORKFLOW_STARTED", workflow_id)
    return handle.id
