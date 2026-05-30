from pprint import pprint
import json
import os
import django
from collections import OrderedDict

from time import sleep
import requests
from loguru import logger
from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from eshop.models import *
from eshop.Utilss.utils import random_code


logger.add("logs/order.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "order_log")
order_log = logger.bind(name="order_log")


setting = Jsonfile.objects.filter(name='Shopsettings').first().json
# print(setting.get('Other').get('TestModus'))
if setting.get('Other').get('TestModus') == True:
    testmod = '.sandbox.'
    api_key = settings.ENV_DICT.kinguin_key_sandbox
else:
    testmod = '.'
    api_key = settings.ENV_DICT.kinguin_key



def getprod(prodid):
    url = f'https://gateway{testmod}kinguin.net/esa/api/v1/products?productId={prodid}'
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    resp = requests.get(url, headers=headers)
    return resp.json()

def order_send(products, ordnr):
        # orderref = random_code(length=6, low=False, up=True, num=True, spchr=False)
    url = f'https://gateway{testmod}kinguin.net/esa/api/v1/order'
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    data = {
        "products":
            
                products
            , 
            "orderExternalId":ordnr
            }
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    return resp.json()


def check(oid, extern):
    if extern == True:
        url = f'https://gateway{testmod}kinguin.net/esa/api/v1/order?orderExternalId={oid}'
    else:
        url = f'https://gateway{testmod}kinguin.net/esa/api/v1/order/{oid}'
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    resp = requests.get(url, headers=headers)
    return resp.json()


def get_keys(oid):
    url = f'https://gateway{testmod}kinguin.net/esa/api/v2/order/{oid}/keys'
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    resp = requests.get(url, headers=headers)
    # order_log.exception()
    return resp.json()

def finalize(order):
    cunt = 0
    while True:
        stat = check(oid=order.get('orderId'), extern=False).get('status')
        order_log.debug(f"stat - {stat}")
        if stat == 'processing':
            sleep(1)
            cunt+=1
        elif stat == 'completed':
            break
        if cunt >= 5:
            break
    return get_keys(order.get('orderId'))


def kinguin_product_order(order, cp_products):
    result = 'ok'
    products = []
    for cp in cp_products:
        product = getprod(cp.product.sku)
        if product.get('item_count') > 0:
            products.append(
                    {
                    "kinguinId":product.get('results')[0].get('kinguinId'),
                    "qty":cp.qty,
                    "name":product.get('results')[0].get('name'),
                    "price":product.get('results')[0].get('price')
                    }
                )
    
    res = order_send(products, order.id)
    if res.get('orderId'):
        resp = finalize(res)
        order_log.debug(f"resp - {resp}")
        if type(resp) == list and len(resp) > 0:
            for cp in cp_products:
                for cod in resp:
                    if cp.product.sku == cod.get('productId'):
                        cr = ProductCode.objects.create(
                            ct_product=cp,
                            cart=order.cart,
                            order=order,
                            pf_order_id=cod.get('offerId'),
                            orderid=order.id,
                            code=cod.get('serial'),
                            serial='',
                            # downloadLink=
                            codeType=cod.get('type')
                        )
                        cp.product_codes.add(cr)
                        cp.save()
                        sleep(1)
        else:
            result = 'error'
            cr = ProductCode.objects.create(
                    ct_product=cp,
                    cart=order.cart,
                    order=order,
                    pf_order_id="cod.get('offerId')",
                    orderid=order.id,
                    code='''Sorry, something went wrong.\n 
                    The transaction will be checked and completed within 48 hours\n 
                    or the amount for the pending delivery will be credited to your digicod wallet.''',
                    serial='',
                    # downloadLink=
                    codeType="cod.get('type')"
                )
            cp.product_codes.add(cr)
            cp.save()
            sleep(1)

    else:
        result = 'error'
    return result





# products = []
# cp_products =['5c9b5f2d2539a4e8f1726251']
# for cp in cp_products:
#     product = getprod(cp)
#     if product.get('item_count') > 0:
#         products.append(
#                 {
#                 "kinguinId":product.get('results')[0].get('kinguinId'),
#                 "qty":2,
#                 "name":product.get('results')[0].get('name'),
#                 "price":product.get('results')[0].get('price')
#                 }
#             )
# res = order_send(products, '86Z9K78H')
# res = check('JS0W4QDBZOJ', extern=False)
# res = get_keys('JS0W4QDBZOJ')
# pprint(res)