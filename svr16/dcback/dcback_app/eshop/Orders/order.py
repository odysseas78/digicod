import sys, os, django, json
from decimal import Decimal
from pprint import pprint
sys.path.insert(0, '/home/dcback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from eshop.Utilss.utils import DictObj
from eshop.wallet.wallet import *
from eshop.models import *
from datetime import datetime, timedelta, timezone
from django.db.models import Q





class Order(object):
    
    def __init__(self):
        pass
    
    
    def create(self, request, del_email):
        if not del_email:
            del_email = request.user.email
        basket = request.user.customer.basket.filter(in_order=False).filter(
                    Q(fingprint=request.COOKIES.get('_polz')) | Q(id=request.COOKIES.get('_ccc'))
                    ).first()
        order = Orders(
            basket=basket,
            del_email=del_email,
            addinfo={'polz':request.COOKIES.get('_polz')}
            )
        order.save()
        order.save()
        order.save()
        basket.order = order
        basket.save()
        order.save()
        return order
    
    
    
    
# qs = Orders.objects.get(id=6)

# qs.save()