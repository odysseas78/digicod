import requests
import os
import hashlib
import hmac
import json
from pprint import pprint
from datetime import datetime
from decimal import Decimal
# from config.settings import env_dict

# from eshop.models import Currency, Order, WalletOrder


# def sign_request(request):
#     json_data = json.dumps(request)
#     key = bytes(os.environ.get('binance_sec_v1'), 'UTF-8')
#     data = bytes(json_data, 'UTF-8')
#     signature = hmac.new(key, msg=data, digestmod=hashlib.sha256).hexdigest()
#     return signature

# sec = os.environ.get('binance_sec_v1')
# key = os.environ.get('binance_key_v1')
sec = env_dict.get('bin_digi_secret')
key = env_dict.get('bin_digi_key')

def sign_request(qs):
    secret = sec
    signature = hmac.new(secret.encode('utf-8'), qs.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature
headers={
        'Content-Type': 'application/json',
        'X-MBX-APIKEY': key
        }

def bgiftoptions(code=None, token=None, referenceNo=None, amount=None):
    '''
      CREATE: token and amount
      VERIFY: referenceNo
      REDEEM: code
       '''
    headers={
        'Content-Type': 'application/json',
        'X-MBX-APIKEY': key
        }
    query_string = f'timestamp={int(datetime.now().timestamp()*1000)}&'
    if token and amount and not referenceNo and not code:
        query_string+=f'token={token}&amount={amount}'
        url = f'https://api.binance.com/sapi/v1/giftcard/createCode?signature={sign_request(query_string)}'
        res = requests.post(url, params=query_string, headers=headers)
    elif referenceNo and not token and not amount and not code:
        query_string+=f'referenceNo={referenceNo}'
        url = f'https://api.binance.com/sapi/v1/giftcard/verify?signature={sign_request(query_string)}'
        res = requests.get(url, params=query_string, headers=headers)
    elif code and not referenceNo and not amount and not token:
        query_string+=f'code={code}'
        url = f'https://api.binance.com/sapi/v1/giftcard/redeemCode?signature={sign_request(query_string)}'
        res = requests.post(url, params=query_string, headers=headers)
    
    return res.json()

# res = bgiftoptions(code=None, token='USDT', referenceNo=None, amount='15')
# res = bgiftoptions(referenceNo='0033000245197936')
# print(res)



def get_prices(token):
    symbol = "BTC"+token
    symbol2 = token+"BTC"
    res = requests.get('https://api.binance.com/api/v3/ticker/price?symbol='+symbol).json()
    if res.get('price'):
        return res
    else:
        res = requests.get('https://api.binance.com/api/v3/ticker/price?symbol='+symbol2).json()
        if res.get('price'):
            return res
    return res

def verify(request, logger):
    '''request | logger'''
    from eshop.models import Jsonfile
    ip = request.META.get('HTTP_X_REAL_IP')
    jsf = Jsonfile.objects.filter(name='bnce_gc').first()
    try:
        if request.data.get('bnce_gc_verify'):
            res = bgiftoptions(referenceNo=request.data.get('bnce_gc_verify'))
            if res.get('code') == '000000' and res.get('data').get('valid'):
              return {'status':'ok',**res.get('data'), **get_prices(res.get('data').get('token'))}
            if res.get('code') == -18001:
                if request.user.id != None:
                    jsf.json.update({request.user.id:datetime.now().timestamp()})
                else:
                    jsf.json.update({request.COOKIE.get('_ccc'):datetime.now().timestamp()})
                jsf.json.update({ip:datetime.now().timestamp()})
                return {'status':'error','msg':'Invalid Gift Card No Entered, Please enter the correct Gift Card no and try again.'}
            if res.get('code') == -18005:
              return {'status':'error', 'msg': 'Too many invalid verify attempts, please try later .'}
        else:
            logger.error('if request.data.get(bnce_gc_verify):')
            return {'status':'error','msg':'There has been an error. Please try again or contact support'}
    except Exception as d:
        logger.exception(d)
        return {'status':'error','msg':'There has been an error. Please try again or contact support'}

def redeem(request, logger):
    '''request | logger'''
    from eshop.models import Jsonfile
    ip = request.META.get('HTTP_X_REAL_IP')
    jsf = Jsonfile.objects.filter(name='bnce_gc').first()
    try:
        if request.data.get('bnce_gc_redeem'):
            res = bgiftoptions(code=request.data.get('code'))
            if res.get('code') == '000000' and res.get('message') == 'success':
              return {'status':'ok',**res.get('data'), **get_prices(res.get('data').get('token'))}
            if res.get('code') == -18001:
                if request.user.id != None:
                    jsf.json.update({request.user.id:datetime.now().timestamp()})
                else:
                    jsf.json.update({request.COOKIE.get('_ccc'):datetime.now().timestamp()})
                jsf.json.update({ip:datetime.now().timestamp()})
                return {'status':'error','msg':'Invalid Gift Card No Entered, Please enter the correct Gift Card no and try again.'}
            if res.get('code') == -18005:
              return {'status':'error', 'msg': 'Too many invalid verify attempts, please try later .'}
        else:
            logger.error('if request.data.get(bnce_gc_verify):')
            return {'status':'error','msg':'There has been an error. Please try again or contact support'}
    except Exception as d:
        logger.exception(d)
        return {'status':'error','msg':'There has been an error. Please try again or contact support'}

# get_prices()




# data = {
#   "env" : {
#     "terminalType": "WEB"
#   },
#   "merchantTradeNo": "9825382937292",
#   "orderAmount": 25.17,
#   "currency": "BUSD",
#   "goods" : {
#     "goodsType": "01",
#     "goodsCategory": "D000",
#     "referenceGoodsId": "7876763A3B",
#     "goodsName": "Ice Cream",
#     "goodsDetail": "Greentea ice cream cone"
#   }
# }
# dfg = bgiftoptions(code=None, token='LTC', referenceNo=None, amount='0.168824')
# pprint(dfg)
# query_string = f'timestamp={int(datetime.now().timestamp()*1000)}'
# url = f'https://bpay.binanceapi.com/binancepay/openapi/v2/order?signature={sign_request(query_string)}'
# res = requests.post(url, params=query_string, headers=headers)
# pprint(res.text)