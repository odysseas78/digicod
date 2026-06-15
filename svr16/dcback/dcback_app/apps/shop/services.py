import uuid, json
from decimal import Decimal, ROUND_HALF_UP
try:
    from http.cookies import SimpleCookie
except ImportError:
    from Cookie import SimpleCookie # type: ignore
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.utils.text import slugify
from django.db.models import Q, OuterRef, Subquery
from rest_framework.permissions import IsAuthenticated, AllowAny
from eshop.order_email_send import orderemail
from datetime import datetime, timedelta, timezone
# from django.utils import timezone

from apps.shop.models import (
    Brand,
    Cart,
    Category,
    FingPrint,
    Product,
    Supplier,
)


class PrepaidForgeError(Exception):
    pass


def normalize_money(value, places="0.0001"):
    return Decimal(str(value)).quantize(Decimal(places), rounding=ROUND_HALF_UP)


def unique_slug(model, value, fallback="item"):
    base = slugify(value) or fallback
    slug = base[:255]
    counter = 2
    while model.objects.filter(slug=slug).exists():
        suffix = f"-{counter}"
        slug = f"{base[:255-len(suffix)]}{suffix}"
        counter += 1
    return slug


# def get_or_create_cart(request):
#     if not request.session.session_key:
#         request.session.create()

#     cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
#     if request.user.is_authenticated:
#         profile, _ = CustomerProfile.objects.get_or_create(
#             user=request.user,
#             defaults={"account_type": CustomerProfile.AccountType.REGISTERED},
#         )
#         if cart.customer_id != profile.id:
#             cart.customer = profile
#             cart.save(update_fields=["customer", "updated_at"])
#     return cart

from django.db import transaction

@transaction.atomic
def sync_products_from_supplier(stocks, products, supplier):
    """
    Synchronisiert Produkte aus einer API-Liste.
    """
    api_skus = {item["product"] for item in stocks}
    
    for item in stocks:
        sku = item["product"]
        
        products_by_sku = {
            item["sku"]: item
            for item in products
        }
        api_product = products_by_sku.get(sku)
        # print(api_product)
        
        category = Category.objects.filter(api_name__in=api_product.get("category"))
        if not category:
            category = Category.objects.bulk_create([
                Category(
                    name=item, api_name=item, slug=unique_slug(Category, item, "category")
                )
                for item in api_product.get("category")
            ])
        
        brand, created = Brand.objects.get_or_create(
            title=api_product.get("brand"),
            defaults={
                "active": True, "supplier":supplier, "in_stock":True, "image":api_product.get("imageUrl"), "slug":unique_slug(Brand, api_product.get("brand"), "brand")
            },
        )
        if created: 
            brand.category.set(category)
            brand.save()
        brand.image = api_product.get("imageUrl")
        brand.save()

        now = timezone.now()
        product = Product.objects.filter(sku=sku).first()
        if product is None:
            # CREATE: alle notwendigen Felder setzen
            product = Product.objects.create(
            brand=brand,
            supplier=supplier,
            title=api_product.get("name"), 
            slug=unique_slug(Product, api_product.get("name")),
            image=api_product.get("imageUrl"),
            sku=sku,
            ean=api_product.get("ean"),
            gtin=api_product.get("gtin"),
            price=item["purchasePrice"],
            prurchase_price=item["purchasePrice"],
            qty=item["quantity"],
            regions=api_product.get("countries"),
            value=json.dumps(api_product.get("faceValue")),
            supplier_product={"product":api_product, "stock":item, "last_synced_at":now.isoformat()},
            active=True,
            in_stock=True
            )
            # for category in categoryList:
            #     product.category.add(category)
            product.category.set(category)
            product.save()
        else:
            # UPDATE: nur bestimmte Felder aktualisieren
            product.supplier_product = {"product":api_product, "stock":item, "last_synced_at":now.isoformat()}
            product.price=item.get("purchasePrice")
            product.prurchase_price=item.get("purchasePrice")
            product.qty=item.get("quantity")
            product.image=api_product.get("imageUrl")
            product.ean=api_product.get("ean")
            product.gtin=api_product.get("gtin")
            product.regions=api_product.get("countries")
            product.value=json.dumps(api_product.get("faceValue"))
            product.in_stock=True
            product.active = True
            product.save()
        
    Product.objects.exclude(
        sku__in=api_skus,
    ).update(active=False, in_stock=False, qty=0)
    


def getCookies(request):
    cookies = SimpleCookie(request.headers.get('set-cookie'))
    polz = request.COOKIES.get('_polz') if request.COOKIES.get('_polz') else cookies.get('_polz').value if cookies.get('_polz') else None
    ccc = request.COOKIES.get('_ccc') if request.COOKIES.get('_ccc') else cookies.get('_ccc').value if cookies.get('_ccc') else None
    return {'polz':polz, 'ccc':ccc}

def get_or_create_cart(request, basketqs=None):
    # logfn1('get_or_create_basket').info(request.META)
    # bqs = basketqs if basketqs else Cart.objects.all()
    fingPrint = getCookies(request).get('polz')
    fingPrintInstance, created = FingPrint.objects.get_or_create(fingprint=fingPrint)
    
    basket_id = getCookies(request).get('ccc')
    if fingPrint == None and basket_id == None:
        return dummybasket
    # logfn1('get_or_create_basket').info(f'{fingPrint} - {basket_id}')
    get_basket = Cart.objects.filter(id=basket_id).first()
    if not get_basket:
        get_basket = Cart.objects.filter(fingprint=fingPrintInstance).first()
    if not get_basket and fingPrint:
        get_basket = Cart(customer=None, fingprint=fingPrintInstance)
        get_basket.save()
        get_basket.save()
        
    basket = Cart.objects.filter(customer=None, updated_at__lt=datetime.now(timezone.utc)-timedelta(days=20))
    if basket.count() > 20:
        basket.delete()
        
    if request.user.is_authenticated:
        if not get_basket.customer:
            get_basket.customer = request.user.customer
            get_basket.save()
            qs = Cart.objects.filter(customer=request.user.customer)
            if qs.count() > 1:
                qs.exclude(id=get_basket.id).delete()
            return get_basket
        else:
            return get_basket
    else:
        get_basket.customer = None
        get_basket.save()
        return get_basket

dummybasket = {
    "basket": {
  "id": 4,
  "currency": {
    "longname": "Euro",
    "shortname": "EUR",
    "price": "1.00000000",
    "sign": "€",
    "image": "/media/currency/flag-round-250.png",
    "image2": None,
    "svg": "",
    "html": ""
  },
  "payment_method": {
    "id": 10,
    "name": "Advanced Cash",
    "desc": "",
    "fee_rate": "4.70",
    "fee_fix": "0.10",
    "image": "https://payop.com/assets/images/methods/advancedCash.jpg",
    "image2": None,
    "svg": "",
    "currencies": [],
    "brands": []
  },
  "products": [],
  "total_products": 0,
  "payment_method_payment": "0.00",
  "wallet_payment": "0.00",
  "total_price": "0.00",
  "final_price": "0.00",
  "process_fee": "0.00",
  "customer": None
},
"message":"",
"type":""
}
# def send_codes_email(order):
#     customer = order.customer.user
#     lines = [
#         f"Hallo {customer.first_name} {customer.last_name},",
#         "",
#         f"deine Bestellung {order.number} wurde erfolgreich geliefert.",
#         "",
#     ]
#     for item in order.items.prefetch_related("codes").all():
#         lines.append(f"{item.product_name} x {item.quantity}")
#         for code in item.codes.all():
#             serial_text = f" | Seriennummer: {code.serial}" if code.serial else ""
#             lines.append(f"Code: {code.code}{serial_text}")
#         lines.append("")

#     send_mail(
#         subject=f"Deine Bestellung {order.number}",
#         message="\n".join(lines),
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         recipient_list=[customer.email],
#         fail_silently=False,
#     )
