import requests
import os
import hashlib
import hmac
import json
from pprint import pprint
from datetime import datetime
from decimal import Decimal
from config.settings import vault_Client.get_secret

# from eshop.models import Currency, Order, WalletOrder


sec = vault_Client.get_secret('binance/digicod', 'binance_sec_v1')
key = vault_Client.get_secret('binance/digicod', 'binance_key_v1')
# sec = os.environ.get('bin_digi_secret')
# key = os.environ.get('bin_digi_key')

def sign_request(qs):
    secret = sec
    signature = hmac.new(secret.encode('utf-8'), qs.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def getAddress(coin):

    headers={
        'Content-Type': 'application/json',
        'X-MBX-APIKEY': key
        }
    query_string = f'timestamp={int(datetime.now().timestamp()*1000)}&coin={coin}'
    url = f'https://api.binance.com/sapi/v1/capital/deposit/address?signature={sign_request(query_string)}'
    res = requests.get(url, params=query_string, headers=headers)
    
    return res.json()


# pprint(getAddress('USDT'))


def getAllCoinsInfo(e):
    ''''''
    headers={
        'Content-Type': 'application/json',
        'X-MBX-APIKEY': key
        }
    query_string = f'timestamp={int(datetime.now().timestamp()*1000)}'
    url = f'https://api.binance.com//sapi/v1/capital/config/getall?signature={sign_request(query_string)}'
    res = requests.get(url, params=query_string, headers=headers)
    
    return res.json()

# tokens = ['BTC', 'USDT', 'XMR', 'SOL']

# for item in getAllCoinsInfo():
#     if item.get('coin') in tokens:
#         pprint(item)
# pprint(getAllCoinsInfo(2, 'USDT'))