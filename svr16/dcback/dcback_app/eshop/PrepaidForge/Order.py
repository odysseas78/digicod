import os
import time
from Utilss.utils import random_code
import django
import requests
from django.conf import settings


os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from eshop.models import *
setting= Jsonfile.objects.filter(name='Shopsettings').first().json
if setting.get('Other').get('TestModus') == True:
    PF_EMAIL = settings.ENV_DICT.TEST_PF_EMAIL
    PF_PASSWORD = settings.ENV_DICT.TEST_PF_PASSWORD
else:
    PF_EMAIL = settings.ENV_DICT.PF_EMAIL
    PF_PASSWORD = settings.ENV_DICT.PF_PASSWORD



def pf_product_order(order, products):

    act_api_token = ShopSetting.objects.get(id=1)
    if act_api_token.pf_api_token_time < int(str(time.time())[:10]) or act_api_token.pf_test_mode != setting.get('Other').get('TestModus'):
        url = 'https://api.prepaidforge.com/v1/1.0/signInWithApi'
        body = {
            "email": PF_EMAIL,
            "password": PF_PASSWORD
        }
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(url, json=body, headers=headers).json()
        act_api_token.pf_api_token_time = int(str(resp['tokenValidUntil'])[:10])
        act_api_token.pf_api_token = resp['apiToken']
        act_api_token.pf_test_mode = setting.get('Other').get('TestModus')
        act_api_token.save()
        act_api_token = ShopSetting.objects.get(id=1)

    findurl = 'https://api.prepaidforge.com/v1/1.0/findStocks'
    createurl = 'https://api.prepaidforge.com/v1/1.0/createApiOrder'
    headers = {'Content-Type': 'application/json',
               'X-PrepaidForge-Api-Token': act_api_token.pf_api_token}

    # order = Order.objects.filter(id=orderid).first()
    # products = CartProduct.objects.filter(cart=order.cart)
    # products = order.cart.products.all()
    result = 'ok'
    for cp in products:
        data = {"types": ["TEXT"], "skus": [cp.product.sku]}
        try:
            resp = requests.post(findurl, json=data, headers=headers).json()
        except:
            result = 'error'
        try:
            data = {"sku": cp.product.sku, "price": resp[0]['purchasePrice'], "codeType": "TEXT"}
        except:
            cp.product.active = False
            cp.product.save()
        i = cp.qty
        while i > 0:
            orderref = random_code(length=6, low=False, up=True, num=True, spchr=False)
            data['customOrderReference'] = f'{order.id}-{orderref}'
            try:
                resp = requests.post(createurl, json=data, headers=headers).json()
            except:
                result = 'error'
                cr = ProductCode.objects.create(
                    ct_product=cp,
                    cart=order.cart,
                    order=order,
                    pf_order_id=0,
                    orderid=0,
                    code='''Sorry, something went wrong.\n 
                    The transaction will be checked and completed within 48 hours\n 
                    or the amount for the pending delivery will be credited to your digicod wallet.''',
                    serial='',
                    # downloadLink=
                    codeType=0
                )
            else:
                try:
                    try:
                        serial = resp['serial']
                    except:
                        serial = ''
                    cr = ProductCode.objects.create(
                        ct_product=cp,
                        cart=order.cart,
                        order=order,
                        pf_order_id=resp['orderReference'],
                        orderid=resp['customOrderReference'],
                        code=resp['code'],
                        serial=serial,
                        # downloadLink=
                        codeType=resp['codeType']
                    )
                except KeyError:
                    result = 'error'
                    cr = ProductCode.objects.create(
                        ct_product=cp,
                        cart=order.cart,
                        order=order,
                        pf_order_id='KeyEerror',
                        orderid=0,
                        code='''Sorry, something went wrong.\n 
                            The transaction will be checked and completed within 48 hours\n 
                            or the amount for the pending delivery will be credited to your digicod wallet.''',
                        serial='',
                        # downloadLink=
                        codeType=0
                    )
            if cr:
                cp.product_codes.add(cr)
                cp.save()
            time.sleep(1)
           
        if result == 'error':
            cr = ProductCode.objects.create(
                    ct_product=cp,
                    cart=order.cart,
                    order=order,
                    pf_order_id=0,
                    orderid=0,
                    code='''Sorry, something went wrong.\n 
                    The transaction will be checked and completed within 48 hours\n 
                    or the amount for the pending delivery will be credited to your digicod wallet.''',
                    serial='',
                    # downloadLink=
                    codeType=0
                )
            if cr:
                cp.product_codes.add(cr)
                cp.save()
        cp.save()
        order.cart.save()
        order.save()
    return result




def get_pf_balance():
    act_api_token = ShopSetting.objects.get(id=1)
    if act_api_token.pf_api_token_time < int(str(time.time())[:10]) or act_api_token.pf_test_mode != setting.get('Other').get('TestModus'):
        url = 'https://api.prepaidforge.com/v1/1.0/signInWithApi'
        body = {
            "email": PF_EMAIL,
            "password": PF_PASSWORD
        }
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(url, json=body, headers=headers).json()
        act_api_token.pf_api_token_time = int(str(resp['tokenValidUntil'])[:10])
        act_api_token.pf_api_token = resp['apiToken']
        act_api_token.pf_test_mode = setting.get('Other').get('TestModus')
        act_api_token.save()
        act_api_token = ShopSetting.objects.get(id=1)

    url = 'https://api.prepaidforge.com/v1/1.0/balance'
    headers = {'Content-Type': 'application/json',
               'X-PrepaidForge-Api-Token': act_api_token.pf_api_token}

    return requests.get(url, headers=headers).json()

# print(get_pf_balance())

    # resp = requests.post(url, json=data, headers=headers).json()

def get_orders(start, end, page):
    act_api_token = ShopSetting.objects.get(id=1)
    if act_api_token.pf_api_token_time < int(str(time.time())[:10]) or act_api_token.pf_test_mode != setting.get('Other').get('TestModus'):
        url = 'https://api.prepaidforge.com/v1/1.0/signInWithApi'
        body = {
            "email": 'admin@digicod.eu',
            "password": 'jEz3xfidZi3SccC'
        }
        headers = {'Content-Type': 'application/json'}
        resp = requests.post(url, json=body, headers=headers).json()
        act_api_token.pf_api_token_time = int(str(resp['tokenValidUntil'])[:10])
        act_api_token.pf_api_token = resp['apiToken']
        act_api_token.pf_test_mode = setting.get('Other').get('TestModus')
        act_api_token.save()
        act_api_token = ShopSetting.objects.get(id=1)

    url = f'https://api.prepaidforge.com/v1/1.0/getApiOrders'
    headers = {'Content-Type': 'application/json',
               'X-PrepaidForge-Api-Token': act_api_token.pf_api_token}
    body = {
            "page": page,
            "startDate": start ,
            "endDate": end
            }

    return requests.post(url, data=json.dumps(body), headers=headers)
