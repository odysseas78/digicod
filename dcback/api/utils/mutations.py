from eshop.models import Cart, Currency, Payment, Product, CartProduct, Basket
from loguru import logger
from django.db.models import Q, OuterRef, Subquery
from rest_framework.permissions import IsAuthenticated, AllowAny
from eshop.order_email_send import orderemail
from datetime import datetime, timedelta, timezone
try:
    from http.cookies import SimpleCookie
except ImportError:
    from Cookie import SimpleCookie # type: ignore

def logfn1(name,path='logs/'):
    logger.add(f"{path}/{name}.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == name)
    return logger.bind(name=name)


def getCookies(request):
    cookies = SimpleCookie(request.headers.get('set-cookie'))
    polz = request.COOKIES.get('_polz') if request.COOKIES.get('_polz') else cookies.get('_polz').value if cookies.get('_polz') else None
    ccc = request.COOKIES.get('_ccc') if request.COOKIES.get('_ccc') else cookies.get('_ccc').value if cookies.get('_ccc') else None
    return {'polz':polz, 'ccc':ccc}

    
    
        
def get_or_create_basket(request, basketqs=None):
    # logfn1('get_or_create_basket').info(request.META)
    bqs = basketqs if basketqs else Basket.objects.filter(in_order=False)
    fingPrint = getCookies(request).get('polz')
    basket_id = getCookies(request).get('ccc')
    if fingPrint == None and basket_id == None:
        return dummybasket
    # logfn1('get_or_create_basket').info(f'{fingPrint} - {basket_id}')
    get_basket = bqs.filter(Q(fingprint=fingPrint) | Q(id=basket_id)).first()
    
    if not get_basket and fingPrint:
        get_basket = Basket(owner=None, fingprint=fingPrint)
        get_basket.save()
        get_basket.save()
        
    basket = bqs.filter(owner=None, updated_at__lt=datetime.now(timezone.utc)-timedelta(days=20))
    if basket.count() > 20:
        basket.delete()
        
    if request.user.is_authenticated:
        if not get_basket.owner:
            get_basket.owner = request.user.customer
            get_basket.save()
            qs = bqs.filter(owner=request.user.customer, in_order=False)
            if qs.count() > 1:
                qs.exclude(id=get_basket.id).delete()
            return get_basket
        else:
            return get_basket
    else:
        get_basket.owner = None
        get_basket.save()
        return get_basket
    


dummybasket = {
    "basket": {
    "id": "",
    "limit": 0.00,
    "total_price": "0.00",
    "final_price": "0.00",
    "process_fee": "0.00",
    "basket_products": {},
    "total_products": 0,
    "payment_method_payment": "0.00",
    "for_anonymous_user": False,
    "owner": None,
    "order": None,
    "payment_method": {},
    "currency": {
            "id": 1,
            "type": "fiat",
            "base": True,
            "longname": "Euro",
            "shortname": "EUR",
            "sign": "€",
            "min_amount": "0.00000000",
            "image": "/media/currency/flag-round-250.png",
            "image2": None,
            "svg": "",
            "html": "",
            "price": "1.00000000",
            "active": True,
            "created_at": "2024-10-01T20:26:54.604738Z",
            "updated_at": "2025-12-25T10:47:24.337825Z"
        },
    "products": []
},
"message":"",
"type":""
}