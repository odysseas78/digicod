import hashlib
import json
import os
from collections import OrderedDict
from pprint import pprint
import django
import jsons
# from config.settings import env_dict
import requests
# import socket
# import socks
# ip='127.0.0.10' # change your proxy's ip
# port = 6000 # change your proxy's port
# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
# socket.socket = socks.socksocket

# os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# django.setup()
env_dict = {}
env_dict["PayOp_APP_ID"]="53108db1-820e-4fe0-b492-5463c33fda85"
env_dict['PayOp_JWT']="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NzUyOTUsImFjY2Vzc1Rva2VuIjoiZWFjN2IyY2I5MGE1MmFhZTBiMGQ5YmIyIiwidG9rZW5JZCI6MjcwMSwid2FsbGV0SWQiOjY3NDMzLCJ0aW1lIjoxNjQ3MzYzNTczLCJleHBpcmVkQXQiOm51bGwsInJvbGVzIjpbMV0sInR3b0ZhY3RvciI6eyJwYXNzZWQiOmZhbHNlfX0.0bfyA-b2aFp_22Gj_FGpNJorWxOg1P9DajY-lXRB1eo"
env_dict['PayOp_SECRET']="4822fdbb3bd95cf9e3b3cc64"

def get_paymethod(title=None, identifier=None):
    url = 'https://payop.com/v1/instrument-settings/payment-methods/available-for-application/'+env_dict.get('PayOp_APP_ID')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+env_dict.get('PayOp_JWT')
    }
    resp = requests.get(url, headers=headers).json()
    if title:
        for item in resp['data']:
            # print(item)
            # print('--------------------------------------------')
            if title and item['title'] == title:
                return item
    elif identifier:
        for item in resp['data']:
            # print(item)
            # print('--------------------------------------------')
            if identifier and item['identifier'] == identifier:
                return item
    else:
        return resp
# with open('payopmethods.json', 'w') as f:
#     f.write(jsons.dumps(get_paymethod()))
# pprint(jsons.load(get_paymethod()))

def gen_signature(amount, currency, orderid):
    order = {'amount': str(amount), 'currency': currency, 'id': str(orderid)}
    order = OrderedDict(sorted(order.items()))
    ordstr = ':'.join(order.values()) + ':'+env_dict.get('PayOp_SECRET')
    h = ordstr.encode()
    hashk = hashlib.sha256(h).hexdigest()
    return hashk


def capiture_transaction(invid):
    url = 'https://payop.com/v1/checkout/capture'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
    "invoiceIdentifier": f"{invid}"

    }
    post_data = json.dumps(data, separators=(',', ':'))
    resp = requests.post(url, headers=headers, data=post_data)
    return resp


def create_invoice(paymentMethod=None, amount=None, currency=None, items=None, orderid=None, useremail=None, 
                   fullname=None, phone=None, resultUrl=None, failPath=None, extrafields=None):
    url = 'https://payop.com/v1/invoices/create'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
    "publicKey": env_dict.get('PayOp_PUBLIC'),
    "order": {
        "id": str(orderid),
        "amount": str(amount),
        "currency": currency,
        "items": items,
        "description": ""
    },
    "signature": gen_signature(amount, currency, orderid),
    "payer": {
        "email": useremail,
        "phone": phone,
        "name": fullname,
        
        "extraFields": [extrafields]
    },
    "paymentMethod": str(paymentMethod),

    "language": "en",
    "resultUrl": resultUrl,
    "failPath": failPath

    }
    post_data = json.dumps(data, separators=(',', ':'))
    resp = requests.post(url, headers=headers, data=post_data)
    return resp
# extraflds = {"date_of_birth": '29.01.1978', "bank_type": '^(SEPA_INSTANT)$'}
# items = [{'id':'21975','name':'Wallet top-up', 'price': '226.35'}]
# result = create_invoice(paymentMethod='200017', amount='226.35', currency='EUR', items=items, orderid='0163245', useremail='coxah@web.de',
#                         fullname='John Milosevic',
#                         resultUrl='https://digicod.eu/orders/8563245', failPath='https://digicod.eu/cancel/8563245', extrafields=extraflds)
# print(result.json())
# print(result.headers)

def get_invoice(id):
    url = 'https://payop.com/v1/invoices/' + id
    headers = {
        'Content-Type': 'application/json',
    }
    resp = requests.get(url, headers=headers)
    return resp

# print(get_invoice('7999f40e-d350-4530-96aa-aee29b7a03b4').json())

def create_checkout(invid, customer,paymentMethod,payCurrency, card, orderid):
    url = 'https://payop.com/v1/checkout/create'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "invoiceIdentifier": str(invid),
        "customer": customer,
        "checkStatusUrl": "https://digicod.eu/payment/"+str(orderid),
    }
    if payCurrency:
        data.update({"payCurrency": payCurrency})
    if paymentMethod:
        data.update({"paymentMethod": paymentMethod})
    if card:
        data.update({"cardToken": card})
    post_data = json.dumps(data, separators=(',', ':'))
    resp = requests.post(url, headers=headers, data=post_data)
    return resp


# result = create_checkout(invid='7999f40e-d350-4530-96aa-aee29b7a03b4', customer={'email':'coxah@web.de', 'name':'John Milosevic'},
#                          paymentMethod=None,payCurrency=None, card=None, orderid='0163245')

# print(result.json())
# print(result.headers)

def check_inv_status(id):
    url = 'https://payop.com/v1/checkout/check-invoice-status/'+id
    headers = {
        'Content-Type': 'application/json',
    }
    resp = requests.get(url, headers=headers)
    return resp

# result = check_inv_status('ee477ca4-b7bd-49f1-acf9-a13983dcb783')
# print(result.json())

