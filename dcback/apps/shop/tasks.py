from celery import shared_task

from .models import CustomerOrder, DeliveredCode, SupplierOrder
from .prepaidforge import PrepaidForgeClient
from .services import PrepaidForgeError, send_codes_email


@shared_task
def sync_products_task():
    client = PrepaidForgeClient()
    client.sync_products()


@shared_task
def process_order_task(order_id):
    order = CustomerOrder.objects.select_related("customer__user").prefetch_related("items__partner_product__partner", "items__codes").get(pk=order_id)
    client = PrepaidForgeClient()

    try:
        order.status = CustomerOrder.Status.PROCESSING
        order.save(update_fields=["status", "updated_at"])

        for item in order.items.select_related("partner_product").all():
            stock_row = client.find_stock_for_sku(item.product_sku)
            latest_price = stock_row.get("purchasePrice")
            latest_quantity = int(stock_row.get("quantity") or 0)
            latest_code_type = stock_row.get("type") or item.supplier_delivery_type

            if latest_quantity < item.quantity:
                raise PrepaidForgeError(f"Not enough stock for {item.product_name}.")

            for index in range(item.quantity):
                custom_reference = item.fulfillment_reference if item.quantity == 1 else f"{item.fulfillment_reference}-{index + 1}"
                response = client.create_api_order(
                    sku=item.product_sku,
                    price=latest_price,
                    code_type=latest_code_type,
                    custom_order_reference=custom_reference,
                )
                DeliveredCode.objects.create(
                    customer_order_item=item,
                    code=str(response.get("code") or ""),
                    serial=str(response.get("serial") or ""),
                    image_url=response.get("image") or "",
                    code_type=response.get("codeType") or latest_code_type,
                    raw_payload=response,
                )

            SupplierOrder.objects.filter(custom_order_reference__startswith=item.fulfillment_reference).update(status=SupplierOrder.Status.COMPLETED)

        order.status = CustomerOrder.Status.COMPLETED
        order.failure_reason = ""
        order.save(update_fields=["status", "failure_reason", "updated_at"])
        send_codes_email(order)
    except PrepaidForgeError as exc:
        order.status = CustomerOrder.Status.FAILED
        order.failure_reason = str(exc)
        order.save(update_fields=["status", "failure_reason", "updated_at"])
        raise
