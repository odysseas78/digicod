import requests

import os
import hashlib
import hmac
import json
from pprint import pprint
from datetime import datetime
from decimal import Decimal
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
# from eshop.models import Currency, Order, WalletOrder
from eshop.models import Currency

# sec = os.environ.get('binance_sec_v1')
# key = os.environ.get('binance_key_v1')

class CryptoPayment:
    sec = env_dict.get('bin_digi_secret')
    key = env_dict.get('bin_digi_key')

    def sign_request(self, qs):
        secret = self.sec
        signature = hmac.new(secret.encode('utf-8'), qs.encode('utf-8'), hashlib.sha256).hexdigest()
        return signature


    def getallcoins(self):

        headers={
            'Content-Type': 'application/json',
            'X-MBX-APIKEY': self.key
            }
        query_string = f'timestamp={int(datetime.now().timestamp()*1000)}'
        url = f'https://api.binance.com/sapi/v1/capital/config/getall?signature={self.sign_request(self, query_string)}'
        res = requests.get(url, params=query_string, headers=headers)
        currencies = Currency.objects.filter(type='crypto')
        def filtercoins(allcoins):
            
            if (allcoins.get('coin'),) in currencies.values_list('shortname'):
                return True
            else:
                return False
        
        coins = []
        for coin in res.json():
            if (coin.get('coin'),) in currencies.values_list('shortname'):
                networks = []
                item = {
                "coin": coin.get('coin'),
                "logo": currencies.filter(shortname=coin.get('coin')).first().image2,
                "depositAllEnable": coin.get('depositAllEnable'),
                "name": coin.get('name'),
                "networks":networks
                }
                
                for network in coin.get('networkList'):
                    if network.get('memoRegex') == '':
                        netitem = {
                        "depositEnable": network.get('depositEnable'),
                        "estimatedArrivalTime": network.get('estimatedArrivalTime'),
                        "minConfirm": network.get('minConfirm'),
                        "network": network.get('network'),
                        "name": network.get('name')
                        }
                        networks.append(netitem)
                coins.append(item)
        return coins

    def getaddress(self, coin, network):
        headers={
            'Content-Type': 'application/json',
            'X-MBX-APIKEY': self.key
            }
        query_string = f'timestamp={int(datetime.now().timestamp()*1000)}&'
        query_string += f"coin={coin}&network={network}"
        url = f'https://api.binance.com/sapi/v1/capital/deposit/address?signature={self.sign_request(self, query_string)}'
        res = requests.get(url, params=query_string, headers=headers)
        
        return res.json()
    

    def getresponse(self):
        res = self.getallcoins(self)
        for coin in res:
            for network in coin.get('networks'):
                address = CryptoPayment.getaddress(CryptoPayment, coin.get('coin'), network.get('network'))
                network.update({"address": address.get('address')})
    
        return res

    
# def filtercoins(allcoins):
#     currencies = Currency.objects.filter(type='crypto')
#     if (allcoins.get('coin'),) in currencies.values_list('shortname'):
#         return allcoins.get('coin')
#     else:
#         return False
    # for coin in res:
    #     networks = []
    #     if (coin.get('coin'),) in currencies.values_list('shortname'):
    #         item = {
    #         "coin": coin.get('coin'),
    #         "logo": currencies.filter(shortname=coin.get('coin')).first().image2,
    #         "depositAllEnable": coin.get('depositAllEnable'),
    #         "name": coin.get('name'),
    #         "networks":networks
    #         }
                        
# cp = CryptoPayment
# res = cp.getresponse(cp)

# pprint(res)




# currencies = Currency.objects.filter(type='crypto').values_list('shortname')
# # pprint(('BTC',) in currencies)
# res = CryptoPayment.getallcoins(CryptoPayment)

# for coin in res:
#     if (coin.get('coin'),) in currencies:
#         print(f"coin: {coin.get('coin')}")
#         print(f"depositAllEnable: {coin.get('depositAllEnable')}")
#         print(f"name: {coin.get('name')}")
#         for network in coin.get('networkList'):
#             if network.get('memoRegex') == '':
#                 address = CryptoPayment.getaddress(CryptoPayment, network.get('coin'), network.get('network'))
#                 print(f"address: {address}")
#                 print(f"addressRegex: {network.get('addressRegex')}")
#                 print(f"coin: {network.get('coin')}")
#                 print(f"depositEnable: {network.get('depositEnable')}")
#                 print(f"estimatedArrivalTime: {network.get('estimatedArrivalTime')}")
#                 print(f"minConfirm: {network.get('minConfirm')}")
#                 print(f"network: {network.get('network')}")
#                 print(f"name: {network.get('name')}")
#                 print("---------------------------------------")
#         print(f"###########################################")



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

