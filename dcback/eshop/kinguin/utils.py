import sys
sys.path.insert(0, '/home/dcback')
import os, sys, django, requests, json
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from datetime import datetime, timedelta
from collections import OrderedDict

from time import sleep
from eshop.models import Order, ProductCode
from eshop.kinguin.order import check, get_keys
from config.settings import vault_Client.get_secret
from eshop.models import Jsonfile


d = 5+6
d

setting = Jsonfile.objects.filter(name='Shopsettings').first().json
if setting.get('Other').get('TestModus') == True:
    testmod = '.sandbox.'
    api_key = vault_Client.get_secret('kinguin', 'kinguin_key_sandbox')
else:
    testmod = '.'
    api_key = vault_Client.get_secret('kinguin', 'kinguin_key')

def get_order(oid):
    from eshop.models import Order
    order = Order.objects.filter(id=oid).first()
    datefrom = order.updated_at - timedelta(minutes=2)
    dateto = order.updated_at + timedelta(minutes=2)
    if order:
        url = f'https://gateway.kinguin.net/esa/api/v1/order?createdAtFrom={str(datefrom)}&createdAtTo={str(dateto)}'
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': api_key
        }
        resp = requests.get(url, headers=headers)
        return resp.json()


def setcodes(oid):
    order = Order.objects.filter(id=oid).first()
    cp_products = order.cart.products.all()
    chk = check(oid, extern=True)
    result = get_keys(chk.get('results')[0].get('orderId'))
    # return result
    for cp in cp_products:
        for cod in result:
            if cp.product.sku == cod.get('productId'):
                obj, cr = ProductCode.objects.get_or_create(
                    code=cod.get('serial'),
                    defaults={
                       "ct_product":cp,
                        "cart":order.cart,
                        "order":order,
                        "pf_order_id":cod.get('offerId'),
                        "orderid":order.id,
                        "serial":'',
                        # downloadLink=
                        "codeType":cod.get('type') 
                    }
                )
                if cr:
                    for c in cp.product_codes.all():
                        if c.code[:6] == "Sorry," or c.code == '' or c.code == None:
                            ProductCode.objects.filter(id=c.id).delete()
                    cp.product_codes.add(obj)
                    cp.save()
                    print(f"add - {obj.code}")
                sleep(1)

# setcodes(877082)
# print(setcodes(873858))
# order = Order.objects.filter(id=870301).first()
# order.cart.products.filter().update(order_price=finalPrice)
