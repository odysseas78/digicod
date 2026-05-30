import requests

import os
import hashlib
import hmac
import json
import string
import random
from pprint import pprint
from datetime import datetime
from decimal import Decimal
from django.conf import settings







length = 32
characters = string.ascii_letters + string.digits
random_string = ''.join(random.choice(characters) for i in range(length))

timestamp = str(int(datetime.now().timestamp()*1000))
nonce = random_string

def sign(payload):
    secret_key = settings.ENV_DICT.bin_merchant_secret.encode('utf-8')
    return  hmac.new(secret_key, payload.encode('utf-8'), hashlib.sha512).hexdigest().upper()

def payload(body):
    return timestamp + "\n" + nonce + "\n" + str(body) + "\n"

def create_order(type, orderqs, amount, currency, urlOk, urlKo, hookUrl):
    goodsName = ''
    if type == 'o':
        for product in orderqs.cart.products.all():
            if goodsName == '':
                goodsName += product.product.title
            else:
                goodsName += ', '+product.product.title
        referenceGoodsId = 'digitalproducts'
    else:
        goodsName = 'digipoints'
        referenceGoodsId = 'digipoints'

    data = {
      "env" : {
        "terminalType": "WEB"
      },
      "merchantTradeNo": str(orderqs.id),
      "orderAmount": str(amount),
      "currency": currency,
      "goods" : {
        "goodsType": "02",
        "goodsCategory": "6000",
        "referenceGoodsId": referenceGoodsId,
        "goodsName": goodsName,
      },
      "returnUrl":urlOk,
      "cancelUrl": urlKo,
      "webhookUrl":hookUrl
      }
    body = json.dumps(data)
    headers={
            'Content-Type': 'application/json',
            'BinancePay-Timestamp': timestamp,
            'BinancePay-Nonce': nonce,
            'BinancePay-Certificate-SN': settings.ENV_DICT.bin_merchant_key,
            'BinancePay-Signature': sign(payload(body))
            }

    url = f'https://bpay.binanceapi.com/binancepay/openapi/v2/order'
    res = requests.post(url, data=body, headers=headers)
    return res.json()


def close_order(merchantTradeNo=None, prepayId=None):
    data = {
      "merchantTradeNo": merchantTradeNo,
      "prepayId": prepayId
    }
    body = json.dumps(data)
    headers={
            'Content-Type': 'application/json',
            'BinancePay-Timestamp': timestamp,
            'BinancePay-Nonce': nonce,
            'BinancePay-Certificate-SN': settings.ENV_DICT.bin_merchant_key,
            'BinancePay-Signature': sign(payload(body))
            }

    url = f'https://bpay.binanceapi.com/binancepay/openapi/order/close'
    res = requests.post(url, data=body, headers=headers)
    return res.json()

# pprint(close_order(merchantTradeNo='466240'))

def query_order(merchantTradeNo=None, prepayId=None):
    data = {
      "merchantTradeNo": merchantTradeNo,
      "prepayId": prepayId
    }
    body = json.dumps(data)
    headers={
            'Content-Type': 'application/json',
            'BinancePay-Timestamp': timestamp,
            'BinancePay-Nonce': nonce,
            'BinancePay-Certificate-SN': settings.ENV_DICT.bin_merchant_key,
            'BinancePay-Signature': sign(payload(body))
            }

    url = f'https://bpay.binanceapi.com/binancepay/openapi/v2/order/query'
    res = requests.post(url, data=body, headers=headers)
    return res.json()



def payer_verify(payerType, accountId):
    data = {
      "payerType": payerType,
      "accountId": accountId
    }
    body = json.dumps(data)
    headers={
            'Content-Type': 'application/json',
            'BinancePay-Timestamp': timestamp,
            'BinancePay-Nonce': nonce,
            'BinancePay-Certificate-SN': settings.ENV_DICT.bin_merchant_key,
            'BinancePay-Signature': sign(payload(body))
            }

    url = f'https://bpay.binanceapi.com/binancepay/openapi/order/payer/verification'
    res = requests.post(url, data=body, headers=headers)
    return res.json()

# pprint(payer_verify(payerType='INDIVIDUAL', accountId='158292251'))


def query_certificate(data):
    
    # body = b'{"bizType":"PAY","data":"{\\"merchantTradeNo\\":\\"870687\\",\\"productType\\":\\"02\\",\\"productName\\":\\"Amazon 25 TRY\\",\\"transactTime\\":1679876794282,\\"tradeType\\":\\"WEB\\",\\"totalFee\\":3.58000000,\\"currency\\":\\"USDT\\",\\"transactionId\\":\\"M_P_219129203579346945\\",\\"openUserId\\":\\"f36fae12c2b40cdbc9ee6ed5402638e0\\",\\"commission\\":0,\\"paymentInfo\\":{\\"payerId\\":158292251,\\"payMethod\\":\\"spot\\",\\"paymentInstructions\\":[{\\"currency\\":\\"LTC\\",\\"amount\\":0.03869345,\\"price\\":92.52211938}],\\"channel\\":\\"DEFAULT\\"}}","bizIdStr":"219129167241265152","bizId":219129167241265152,"bizStatus":"PAY_SUCCESS"}'
    data2 = json.loads(data)
    body = json.dumps(data2)
    headers={
            'Content-Type': 'application/json',
            'BinancePay-Timestamp': timestamp,
            'BinancePay-Nonce': nonce,
            'BinancePay-Certificate-SN': settings.ENV_DICT.bin_merchant_key,
            'BinancePay-Signature': sign(payload(body))
            }

    url = f'https://bpay.binanceapi.com/binancepay/openapi/certificates'
    res = requests.post(url, data=body, headers=headers)
    return res.json()

# pprint(query_order('870680'))




# header = {'Host': 'odys.digicod.eu', 'X-Real-Ip': '10.0.2.1', 'X-Forwarded-For': '10.0.2.1', 'X-Forwarded-Proto': 'https', 'Connection': 'close', 'Content-Length': '594', 'Binancepay-Certificate-Sn': '31BEF298427BE2F0B98DFA3A523D7501', 'Binancepay-Nonce': 'zREdMIt0y4Y695XvDM9YjeV5FwpwXun3', 'Binancepay-Timestamp': '1679876824832', 'Binancepay-Signature': 'VDzTLsGQeTkN0Zn4tGwwpWuGUpXt3XfNvWOn25wvFEAw4oA/mOjgGZhi9p3kb2UwFtSX7n8O0FIQb6gpUU8uuOVspZ0OZso+1nu/OWOFDriDN3txjew8uTQicuSMj0+b6QxcnSrXGbwnjqc7VcHcu3NtRqSdGr2XghNHgQZnp8ImhbEcsJD/QpB++b4KAMpz0XhyQ9Y1UMKHZcFQftOAdXx0Jp85guukVIWnfx4QkVdeA6atUSXBFUt3WgtBGXYODGQVV0Mne0Koc5eHCTZ+3lG9P4udwaWuM+33FcwvVBx+sgubLeA2HH8ipdaTcrWyw8XUt61Twm7cDif7tvvuvwdnICr9gwITKFBN5Z0NZLrGu/mkqVyMpCIradBhvoECQFhfBcP34SE4ufe3Klyu9+uEyZz1wZj5zs4ofhKxeBo85hpKONbBCOQNDZs/vX7A4ycSwaXPEXa+w8AHg8i3kMre5JY7l7o7oLY7Ca8EHI7qO/Bu5MRGOO9flh7ojOb1MXhEbbGuj3R8tNHAvUNBauYbdP9kySnuD20Si+XL8kU6f/f8sYhni2nNBLq5aN6TbLGkwXrQ6ICau2q511u8hIWwr+2YKAZmW1w4Yqdf3nHxAkeE+AJnJPCcLAEYQYRZd6JivjiNlCv104fGweMRxWXcJaNMSCnRcG+1AL9E6ZY=', 'Content-Type': 'application/json; charset=utf-8', 'Accept-Encoding': 'gzip', 'User-Agent': 'okhttp/3.14.9'}


# body = b'{"bizType":"PAY","data":"{\\"merchantTradeNo\\":\\"870687\\",\\"productType\\":\\"02\\",\\"productName\\":\\"Amazon 25 TRY\\",\\"transactTime\\":1679876794282,\\"tradeType\\":\\"WEB\\",\\"totalFee\\":3.58000000,\\"currency\\":\\"USDT\\",\\"transactionId\\":\\"M_P_219129203579346945\\",\\"openUserId\\":\\"f36fae12c2b40cdbc9ee6ed5402638e0\\",\\"commission\\":0,\\"paymentInfo\\":{\\"payerId\\":158292251,\\"payMethod\\":\\"spot\\",\\"paymentInstructions\\":[{\\"currency\\":\\"LTC\\",\\"amount\\":0.03869345,\\"price\\":92.52211938}],\\"channel\\":\\"DEFAULT\\"}}","bizIdStr":"219129167241265152","bizId":219129167241265152,"bizStatus":"PAY_SUCCESS"}'

# # pprint(query_certificate(body))
# payld = header.get('Binancepay-Timestamp') + "\n" + header.get('Binancepay-Nonce') + "\n" + json.dumps(json.loads(body)) + "\n"

# def openssl_verify(payload, decodedSignature, publicKey):
#     # Dekodieren des Base64-codierten Signature-Strings
#     signature = decodedSignature.encode('utf-8')
    
#     # Erstellen des öffentlichen Schlüssels aus der PEM-codierten Key-Datei
#     public_key = serialization.load_pem_public_key(publicKey.encode('utf-8'))
    
#     # Berechnen des Hash-Werts des Payloads
#     hash = hashes.Hash(hashes.SHA256())
#     hash.update(payload.encode('utf-8'))
#     digest = hash.finalize()
    
#     # Verifizieren der Signatur
#     return public_key.verify(signature, digest, asym.padding.PKCS1v15(), hashes.SHA256())


# result = openssl_verify(
#     payload=payld,
#     decodedSignature=header.get('Binancepay-Signature'),
#     publicKey=query_certificate(body).get('data')[0].get('certPublic'), 
#     )
# print(result)


# def verify_signature(pub_key_str, decoded_signature, payload):
#     pub_key_obj = RSA.importKey(pub_key_str)
#     pub_key = PKCS1_v1_5.new(pub_key_obj)

#     payload_bytes = payload.encode('utf-8')
#     h = SHA256.new(payload_bytes)
#     return pub_key.verify(h, decoded_signature)

# result = verify_signature(
#     payload=payld,
#     decoded_signature=header.get('Binancepay-Signature'),
#     pub_key_str=query_certificate(body).get('data')[0].get('certPublic'), 
#     )
# pprint(result)