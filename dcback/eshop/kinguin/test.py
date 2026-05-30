from pprint import pprint
import json
import os
from collections import OrderedDict
from time import sleep
import requests
from config.settings import vault_Client.get_secret



def getprod():
    url = 'https://gateway.kinguin.net/esa/api/v1/products?platform=Kinguin&name=Card&name=Gift'
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': vault_Client.get_secret('kinguin', 'kinguin_key')
    }
    resp = requests.get(url, headers=headers)
    return resp.json()

def sgetprod(prodid):
    url = f'https://gateway.sandbox.kinguin.net/esa/api/v1/products?productId={prodid}'
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': vault_Client.get_secret('kinguin', 'kinguin_key_sandbox')
    }
    resp = requests.get(url, headers=headers)
    return resp.json()

def order(prodId, qty, ordnr):
    product = sgetprod(prodId)
    if product.get('item_count') > 0:
        url = 'https://gateway.sandbox.kinguin.net/esa/api/v1/order'
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': vault_Client.get_secret('kinguin', 'kinguin_key_sandbox')
        }
        data = {
            "products":
                [
                    {
                    "kinguinId":product.get('results')[0].get('kinguinId'),
                    "qty":qty,
                    "name":product.get('results')[0].get('name'),
                    "price":product.get('results')[0].get('price')
                    }
                ], 
                "orderExternalId":ordnr
                }
        resp = requests.post(url, data=json.dumps(data), headers=headers)
        return resp.json()
    else:
        return None


def check(oid):
    url = f'https://gateway.sandbox.kinguin.net/esa/api/v1/order/{oid}'
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': vault_Client.get_secret('kinguin', 'kinguin_key_sandbox')
    }
    resp = requests.get(url, headers=headers)
    return resp.json()


def keys(oid):
    url = f'https://gateway.sandbox.kinguin.net/esa/api/v2/order/{oid}/keys'
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': vault_Client.get_secret('kinguin', 'kinguin_key_sandbox')
    }
    resp = requests.get(url, headers=headers)
    return resp.json()

def finalize(prodid, qty, ordnr):
    ordr = order(prodid, qty, ordnr)
    
    if ordr:
        cunt = 0
        while True:
            if cunt >=10:
                return {'An error has occurred, please try again.'}
            stat = check(ordr.get('orderId')).get('status')
            if stat == 'processing':
                sleep(2)
                cunt+=1
            elif stat == 'completed':
                return keys(ordr.get('orderId'))
            else:
                return stat.json()
# pprint(finalize('5c9b768c2539a4e8f1831c70',2,'858999'))
# pprint(check('SHVDJMZZACU'))
# pprint(sgetprod('5eecdf4f771dd0a5ca63b8b6').get('results')[0].get('kinguinId'))


# for item in getprod().get('results'):
#     pprint(item.get('name'))