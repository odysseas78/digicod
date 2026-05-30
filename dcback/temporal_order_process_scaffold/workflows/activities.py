from __future__ import annotations

from decimal import Decimal
from typing import Any
from asgiref.sync import sync_to_async
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.utils import timezone
from temporalio import activity

from integrations.prepaidforge.client import PrepaidForgeClient, PrepaidForgeError, PrepaidForgePurchaseUncertainError
from orders.crypto import encrypt_text, decrypt_text
from orders.models import (
    EmailDelivery, EmailDeliveryStatus, Order, OrderItem, OrderStatus,
    ProductStockStatus, PurchasedCode, SupplierCode, SupplierProduct,
    SupplierPurchase, SupplierPurchaseStatus, add_order_event,
)

@sync_to_async
def load_order_snapshot(order_id: str) -> dict[str, Any]:
    order = Order.objects.prefetch_related("items").get(id=order_id)
    return {
        "order_id": str(order.id),
        "status": order.status,
        "customer_email": order.customer_email,
        "total": str(order.total),
        "currency": order.currency,
        "items": [
            {"order_item_id": str(item.id), "supplier": item.supplier_product.supplier, "supplier_sku": item.supplier_sku_snapshot, "quantity": item.quantity}
            for item in order.items.all()
        ],
    }

@sync_to_async
def verify_payment(order_id: str) -> dict[str, Any]:
    order = Order.objects.get(id=order_id)
    if order.status not in [OrderStatus.PAYMENT_AUTHORIZED, OrderStatus.PAID, OrderStatus.FULFILLMENT_STARTED]:
        order.status = OrderStatus.FAILED_NEEDS_REVIEW
        order.failure_reason = f"Payment is not ready. Current status: {order.status}"
        order.save(update_fields=["status", "failure_reason", "updated_at"])
        add_order_event(order, "PAYMENT_NOT_READY", order.failure_reason)
        raise RuntimeError(order.failure_reason)
    add_order_event(order, "PAYMENT_VERIFIED", "Payment verified or authorized")
    return {"ok": True}

@sync_to_async
def final_availability_check(order_id: str) -> dict[str, Any]:
    order = Order.objects.prefetch_related("items__supplier_product").get(id=order_id)
    problems = []
    for item in order.items.all():
        supplier = item.supplier_product
        if not supplier.supplier_active or supplier.stock_status == ProductStockStatus.OUT_OF_STOCK:
            problems.append({"order_item_id": str(item.id), "supplier_sku": item.supplier_sku_snapshot, "reason": "out_of_stock_or_inactive"})
        elif supplier.stock_quantity is not None and item.quantity > supplier.stock_quantity:
            problems.append({"order_item_id": str(item.id), "supplier_sku": item.supplier_sku_snapshot, "reason": "insufficient_stock", "requested": item.quantity, "available": supplier.stock_quantity})
    if problems:
        order.status = OrderStatus.REFUND_PENDING
        order.failure_reason = "Final supplier availability check failed"
        order.last_error_payload = {"problems": problems}
        order.save(update_fields=["status", "failure_reason", "last_error_payload", "updated_at"])
        add_order_event(order, "FINAL_AVAILABILITY_FAILED", "Final supplier availability check failed", {"problems": problems})
        return {"ok": False, "problems": problems}
    order.status = OrderStatus.SUPPLIER_PURCHASE_PENDING
    order.save(update_fields=["status", "updated_at"])
    add_order_event(order, "FINAL_AVAILABILITY_OK", "All items are available")
    return {"ok": True, "problems": []}

@activity.defn
async def act_load_order_snapshot(order_id: str) -> dict[str, Any]:
    return await load_order_snapshot(order_id)

@activity.defn
async def act_verify_payment(order_id: str) -> dict[str, Any]:
    return await verify_payment(order_id)

@activity.defn
async def act_final_availability_check(order_id: str) -> dict[str, Any]:
    return await final_availability_check(order_id)

@activity.defn
async def act_purchase_and_store_supplier_codes(order_id: str) -> dict[str, Any]:
    return await _purchase_and_store_supplier_codes(order_id)

@sync_to_async
def _get_order_items(order_id: str) -> list[str]:
    return list(OrderItem.objects.filter(order_id=order_id).order_by("id").values_list("id", flat=True))

async def _purchase_and_store_supplier_codes(order_id: str) -> dict[str, Any]:
    client = PrepaidForgeClient()
    item_ids = await _get_order_items(order_id)
    purchase_ids = []
    for item_id in item_ids:
        result = await _purchase_single_item(client, order_id, str(item_id))
        purchase_ids.append(result["supplier_purchase_id"])
    await _mark_order_codes_stored(order_id)
    return {"ok": True, "supplier_purchase_ids": purchase_ids}

@sync_to_async
@transaction.atomic
def _prepare_supplier_purchase(order_id: str, order_item_id: str) -> dict[str, Any]:
    order = Order.objects.select_for_update().get(id=order_id)
    item = OrderItem.objects.select_related("supplier_product").select_for_update().get(id=order_item_id, order=order)
    existing_success = SupplierPurchase.objects.filter(order=order, order_item=item, status=SupplierPurchaseStatus.SUCCESS).first()
    if existing_success:
        return {"skip": True, "supplier_purchase_id": str(existing_success.id), "reason": "already_successful"}
    idempotency_key = f"order-{order.id}-item-{item.id}"
    purchase, _ = SupplierPurchase.objects.get_or_create(
        idempotency_key=idempotency_key,
        defaults={
            "order": order,
            "order_item": item,
            "supplier": item.supplier_product.supplier,
            "supplier_sku": item.supplier_sku_snapshot,
            "quantity": item.quantity,
            "status": SupplierPurchaseStatus.PENDING,
            "request_payload": {"supplier_sku": item.supplier_sku_snapshot, "quantity": item.quantity, "client_reference": idempotency_key},
        },
    )
    if purchase.status == SupplierPurchaseStatus.SUCCESS:
        return {"skip": True, "supplier_purchase_id": str(purchase.id), "reason": "already_successful"}
    if purchase.status == SupplierPurchaseStatus.UNCERTAIN:
        raise RuntimeError(f"Supplier purchase is uncertain and needs admin review: {purchase.id}")
    add_order_event(order, "SUPPLIER_PURCHASE_PREPARED", str(purchase.id), {"order_item_id": str(item.id)})
    return {"skip": False, "supplier_purchase_id": str(purchase.id), "supplier": purchase.supplier, "supplier_sku": purchase.supplier_sku, "quantity": purchase.quantity, "idempotency_key": purchase.idempotency_key}

@sync_to_async
@transaction.atomic
def _store_successful_purchase(*, purchase_id: str, supplier_order_id: str, raw_response: dict[str, Any], codes: list[dict[str, Any]]) -> dict[str, Any]:
    purchase = SupplierPurchase.objects.select_for_update().select_related("order", "order_item").get(id=purchase_id)
    if purchase.status == SupplierPurchaseStatus.SUCCESS:
        return {"supplier_purchase_id": str(purchase.id), "already_stored": True}
    purchase.status = SupplierPurchaseStatus.SUCCESS
    purchase.supplier_order_id = supplier_order_id
    purchase.response_payload = raw_response
    purchase.error_message = ""
    purchase.succeeded_at = timezone.now()
    purchase.save(update_fields=["status", "supplier_order_id", "response_payload", "error_message", "succeeded_at", "updated_at"])
    for code in codes:
        PurchasedCode.objects.create(
            order=purchase.order,
            order_item=purchase.order_item,
            supplier_purchase=purchase,
            code_encrypted=encrypt_text(code.get("code", "")),
            pin_encrypted=encrypt_text(code.get("pin", "")),
            serial_number_encrypted=encrypt_text(code.get("serial_number", "")),
        )
    add_order_event(purchase.order, "SUPPLIER_PURCHASE_SUCCESS", str(purchase.id), {"supplier_order_id": supplier_order_id, "codes_count": len(codes)})
    return {"supplier_purchase_id": str(purchase.id), "already_stored": False}

@sync_to_async
@transaction.atomic
def _store_failed_purchase(purchase_id: str, error: str, uncertain: bool = False) -> None:
    purchase = SupplierPurchase.objects.select_for_update().select_related("order").get(id=purchase_id)
    purchase.status = SupplierPurchaseStatus.UNCERTAIN if uncertain else SupplierPurchaseStatus.FAILED
    purchase.error_message = error
    purchase.uncertain_reason = error if uncertain else ""
    purchase.save(update_fields=["status", "error_message", "uncertain_reason", "updated_at"])
    order = purchase.order
    order.status = OrderStatus.SUPPLIER_PURCHASE_UNCERTAIN if uncertain else OrderStatus.FAILED_NEEDS_REVIEW
    order.failure_reason = error
    order.last_error_payload = {"supplier_purchase_id": str(purchase.id), "uncertain": uncertain, "error": error}
    order.save(update_fields=["status", "failure_reason", "last_error_payload", "updated_at"])
    add_order_event(order, "SUPPLIER_PURCHASE_UNCERTAIN" if uncertain else "SUPPLIER_PURCHASE_FAILED", error, {"supplier_purchase_id": str(purchase.id)})

async def _purchase_single_item(client: PrepaidForgeClient, order_id: str, order_item_id: str) -> dict[str, Any]:
    prepared = await _prepare_supplier_purchase(order_id, order_item_id)
    if prepared["skip"]:
        return {"supplier_purchase_id": prepared["supplier_purchase_id"], "skipped": True}
    purchase_id = prepared["supplier_purchase_id"]
    if prepared["supplier"] != SupplierCode.PREPAIDFORGE:
        await _store_failed_purchase(purchase_id, f"Unsupported supplier: {prepared['supplier']}")
        raise RuntimeError(f"Unsupported supplier: {prepared['supplier']}")
    try:
        result = await client.purchase_product(sku=prepared["supplier_sku"], quantity=prepared["quantity"], client_reference=prepared["idempotency_key"], idempotency_key=prepared["idempotency_key"])
    except PrepaidForgePurchaseUncertainError as exc:
        await _store_failed_purchase(purchase_id, str(exc), uncertain=True)
        raise
    except PrepaidForgeError as exc:
        await _store_failed_purchase(purchase_id, str(exc), uncertain=False)
        raise
    await _store_successful_purchase(
        purchase_id=purchase_id,
        supplier_order_id=result.supplier_order_id,
        raw_response=result.raw,
        codes=[{"code": c.code, "pin": c.pin, "serial_number": c.serial_number, "expires_at": c.expires_at} for c in result.codes],
    )
    return {"supplier_purchase_id": purchase_id, "skipped": False}

@sync_to_async
@transaction.atomic
def _mark_order_codes_stored(order_id: str) -> None:
    order = Order.objects.select_for_update().get(id=order_id)
    if not order.purchased_codes.exists():
        raise RuntimeError("No purchased codes were stored")
    order.status = OrderStatus.CODES_STORED
    order.save(update_fields=["status", "updated_at"])
    add_order_event(order, "CODES_STORED", "Supplier codes stored encrypted")

@activity.defn
async def act_send_order_codes_email(order_id: str) -> dict[str, Any]:
    return await _send_order_codes_email(order_id)

@sync_to_async
@transaction.atomic
def _prepare_email_delivery(order_id: str) -> str:
    order = Order.objects.select_for_update().get(id=order_id)
    order.status = OrderStatus.EMAIL_PENDING
    order.save(update_fields=["status", "updated_at"])
    delivery, _ = EmailDelivery.objects.get_or_create(order=order, template="order_codes", recipient=order.customer_email, defaults={"status": EmailDeliveryStatus.PENDING})
    delivery.attempts += 1
    delivery.save(update_fields=["attempts", "updated_at"])
    add_order_event(order, "EMAIL_ATTEMPT", f"Attempt {delivery.attempts}")
    return str(delivery.id)

@sync_to_async
def _render_email(order_id: str) -> dict[str, str]:
    order = Order.objects.prefetch_related("items", "purchased_codes").get(id=order_id)
    lines = ["Hallo,", "", f"vielen Dank für deine Bestellung {order.id}.", "", "Deine Produktcodes:", ""]
    for code in order.purchased_codes.select_related("order_item").all():
        lines.append(f"Produkt: {code.order_item.product_name_snapshot}")
        lines.append(f"Code: {decrypt_text(code.code_encrypted)}")
        pin = decrypt_text(code.pin_encrypted)
        serial = decrypt_text(code.serial_number_encrypted)
        if pin: lines.append(f"PIN: {pin}")
        if serial: lines.append(f"Serial: {serial}")
        lines.append("")
    return {"subject": f"Deine Bestellung {order.id}", "text_body": "\n".join(lines), "html_body": "<br>".join(lines), "recipient": order.customer_email}

@sync_to_async
@transaction.atomic
def _mark_email_sent(delivery_id: str, provider_message_id: str = "") -> None:
    delivery = EmailDelivery.objects.select_for_update().select_related("order").get(id=delivery_id)
    delivery.status = EmailDeliveryStatus.SENT
    delivery.provider_message_id = provider_message_id
    delivery.last_error = ""
    delivery.sent_at = timezone.now()
    delivery.save(update_fields=["status", "provider_message_id", "last_error", "sent_at", "updated_at"])
    order = delivery.order
    order.status = OrderStatus.EMAIL_SENT
    order.save(update_fields=["status", "updated_at"])
    PurchasedCode.objects.filter(order=order, delivered_at__isnull=True).update(delivered_at=timezone.now(), email_message_id=provider_message_id)
    add_order_event(order, "EMAIL_SENT", "Order code email sent", {"delivery_id": str(delivery.id)})

@sync_to_async
@transaction.atomic
def _mark_email_failed(delivery_id: str, error: str) -> None:
    delivery = EmailDelivery.objects.select_for_update().select_related("order").get(id=delivery_id)
    delivery.status = EmailDeliveryStatus.FAILED
    delivery.last_error = error
    delivery.save(update_fields=["status", "last_error", "updated_at"])
    order = delivery.order
    order.status = OrderStatus.EMAIL_PENDING
    order.failure_reason = f"Email failed: {error}"
    order.save(update_fields=["status", "failure_reason", "updated_at"])
    add_order_event(order, "EMAIL_FAILED", error, {"delivery_id": str(delivery.id)})

async def _send_order_codes_email(order_id: str) -> dict[str, Any]:
    delivery_id = await _prepare_email_delivery(order_id)
    rendered = await _render_email(order_id)
    try:
        msg = EmailMultiAlternatives(subject=rendered["subject"], body=rendered["text_body"], from_email=None, to=[rendered["recipient"]])
        msg.attach_alternative(rendered["html_body"], "text/html")
        sent_count = await sync_to_async(msg.send)(fail_silently=False)
        if sent_count < 1:
            raise RuntimeError("Django email backend returned sent_count=0")
    except Exception as exc:
        await _mark_email_failed(delivery_id, str(exc))
        raise
    await _mark_email_sent(delivery_id, "")
    return {"ok": True, "delivery_id": delivery_id}

@activity.defn
async def act_mark_order_completed(order_id: str) -> dict[str, Any]:
    return await _mark_order_completed(order_id)

@sync_to_async
@transaction.atomic
def _mark_order_completed(order_id: str) -> dict[str, Any]:
    order = Order.objects.select_for_update().get(id=order_id)
    order.status = OrderStatus.COMPLETED
    order.completed_at = timezone.now()
    order.save(update_fields=["status", "completed_at", "updated_at"])
    add_order_event(order, "ORDER_COMPLETED", "Order completed")
    return {"ok": True}

@activity.defn
async def act_mark_order_needs_review(order_id: str, reason: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return await _mark_order_needs_review(order_id, reason, payload or {})

@sync_to_async
@transaction.atomic
def _mark_order_needs_review(order_id: str, reason: str, payload: dict[str, Any]) -> dict[str, Any]:
    order = Order.objects.select_for_update().get(id=order_id)
    order.status = OrderStatus.FAILED_NEEDS_REVIEW
    order.failure_reason = reason
    order.last_error_payload = payload
    order.save(update_fields=["status", "failure_reason", "last_error_payload", "updated_at"])
    add_order_event(order, "ORDER_NEEDS_REVIEW", reason, payload)
    return {"ok": True}

@activity.defn
async def act_sync_prepaidforge_catalog() -> dict[str, Any]:
    client = PrepaidForgeClient()
    products = await client.list_products()
    return await _upsert_supplier_products([
        {"sku": p.sku, "name": p.name, "brand": p.brand, "category": p.category, "currency": p.currency, "purchase_price": str(p.purchase_price), "stock_status": p.stock_status, "stock_quantity": p.stock_quantity, "active": p.active, "raw": p.raw}
        for p in products
    ])

@sync_to_async
@transaction.atomic
def _upsert_supplier_products(products: list[dict[str, Any]]) -> dict[str, Any]:
    now = timezone.now()
    seen_skus = set()
    created = 0
    updated = 0
    for row in products:
        sku = row["sku"]
        seen_skus.add(sku)
        purchase_price = Decimal(str(row["purchase_price"]))
        obj, was_created = SupplierProduct.objects.get_or_create(
            supplier=SupplierCode.PREPAIDFORGE,
            supplier_sku=sku,
            defaults={
                "name_original": row["name"], "brand": row["brand"], "category": row["category"], "currency": row["currency"],
                "purchase_price": purchase_price, "stock_status": row["stock_status"], "stock_quantity": row["stock_quantity"],
                "supplier_active": row["active"], "raw_payload": row["raw"], "last_synced_at": now, "last_seen_at": now,
            },
        )
        if was_created:
            created += 1
            continue
        changed_price = obj.purchase_price != purchase_price
        changed_stock = obj.stock_status != row["stock_status"] or obj.stock_quantity != row["stock_quantity"]
        obj.name_original = row["name"]
        obj.brand = row["brand"]
        obj.category = row["category"]
        obj.currency = row["currency"]
        obj.purchase_price = purchase_price
        obj.stock_status = row["stock_status"]
        obj.stock_quantity = row["stock_quantity"]
        obj.supplier_active = row["active"]
        obj.raw_payload = row["raw"]
        obj.last_synced_at = now
        obj.last_seen_at = now
        if changed_price: obj.last_price_changed_at = now
        if changed_stock: obj.last_stock_changed_at = now
        obj.save()
        updated += 1
    if seen_skus:
        SupplierProduct.objects.filter(supplier=SupplierCode.PREPAIDFORGE).exclude(supplier_sku__in=seen_skus).update(supplier_active=False, last_synced_at=now)
    return {"created": created, "updated": updated, "seen": len(seen_skus)}
