from __future__ import annotations

import uuid
from decimal import Decimal
from typing import Any
from django.db import transaction
from django.utils import timezone
from orders.models import CartValidationStatus, Order, OrderItem, OrderStatus, ProductStockStatus, ShopProduct, add_order_event

def _line_total(unit_price: Decimal, quantity: int) -> Decimal:
    return (unit_price * Decimal(quantity)).quantize(Decimal("0.01"))

def validate_cart(cart_items: list[dict[str, Any]]) -> dict[str, Any]:
    changes = []
    normalized_items = []
    total = Decimal("0.00")

    for item in cart_items:
        product_id = item["shop_product_id"]
        requested_quantity = int(item.get("quantity", 1))
        client_price = Decimal(str(item.get("unit_price", "0.00")))

        try:
            product = ShopProduct.objects.select_related("supplier_product").get(id=product_id, active_in_shop=True)
        except ShopProduct.DoesNotExist:
            changes.append({"product_id": str(product_id), "type": "removed", "reason": "product_not_available"})
            continue

        supplier = product.supplier_product

        if not supplier.supplier_active or supplier.stock_status == ProductStockStatus.OUT_OF_STOCK:
            changes.append({"product_id": str(product.id), "type": "removed", "reason": "out_of_stock", "name": product.public_name})
            continue

        quantity = max(1, requested_quantity)
        if quantity > product.max_quantity_per_order:
            changes.append({"product_id": str(product.id), "type": "quantity_changed", "old_quantity": requested_quantity, "new_quantity": product.max_quantity_per_order})
            quantity = product.max_quantity_per_order

        if supplier.stock_quantity is not None and quantity > supplier.stock_quantity:
            changes.append({"product_id": str(product.id), "type": "quantity_changed", "old_quantity": quantity, "new_quantity": supplier.stock_quantity, "reason": "supplier_stock_limit"})
            quantity = supplier.stock_quantity

        if quantity <= 0:
            changes.append({"product_id": str(product.id), "type": "removed", "reason": "zero_stock"})
            continue

        current_price = product.selling_price
        if current_price != client_price:
            changes.append({"product_id": str(product.id), "type": "price_changed", "old_price": str(client_price), "new_price": str(current_price)})

        line_total = _line_total(current_price, quantity)
        total += line_total
        normalized_items.append({
            "shop_product_id": str(product.id),
            "supplier_product_id": supplier.id,
            "supplier": supplier.supplier,
            "supplier_sku": supplier.supplier_sku,
            "name": product.public_name,
            "quantity": quantity,
            "unit_price": str(current_price),
            "line_total": str(line_total),
            "currency": product.selling_currency,
            "supplier_purchase_price": str(supplier.purchase_price),
        })

    status = CartValidationStatus.CART_CHANGED if changes else CartValidationStatus.OK
    return {
        "status": status,
        "cart_token": uuid.uuid4().hex,
        "expires_at": (timezone.now() + timezone.timedelta(minutes=10)).isoformat(),
        "changes": changes,
        "items": normalized_items,
        "total": str(total.quantize(Decimal("0.01"))),
        "currency": normalized_items[0]["currency"] if normalized_items else "EUR",
    }

@transaction.atomic
def create_order_from_validated_cart(*, customer_email: str, validated_cart: dict[str, Any], customer_user_id: int | None = None) -> Order:
    if validated_cart["status"] != CartValidationStatus.OK:
        raise ValueError("Cannot create order from changed cart. Customer must confirm new cart first.")

    order = Order.objects.create(
        customer_email=customer_email,
        customer_user_id=customer_user_id,
        status=OrderStatus.CONFIRMED,
        currency=validated_cart.get("currency", "EUR"),
        subtotal=Decimal(str(validated_cart["total"])),
        total=Decimal(str(validated_cart["total"])),
        cart_token=validated_cart["cart_token"],
        cart_confirmed_at=timezone.now(),
        order_snapshot=validated_cart,
    )

    for row in validated_cart["items"]:
        product = ShopProduct.objects.select_related("supplier_product").get(id=row["shop_product_id"])
        supplier = product.supplier_product
        OrderItem.objects.create(
            order=order,
            shop_product=product,
            supplier_product=supplier,
            product_name_snapshot=row["name"],
            supplier_sku_snapshot=row["supplier_sku"],
            quantity=int(row["quantity"]),
            unit_price=Decimal(str(row["unit_price"])),
            line_total=Decimal(str(row["line_total"])),
            supplier_purchase_price_snapshot=Decimal(str(row["supplier_purchase_price"])),
            raw_snapshot=row,
        )

    add_order_event(order, "ORDER_CREATED", "Order created from validated cart", validated_cart)
    return order
