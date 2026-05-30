import base64
import hashlib
import hmac
import os
import time
import urllib.parse
from config.settings import vault_Client.get_secret
import django
import requests

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


def get_kraken_signature(urlpath, data, secret):

    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


# Read Kraken API key and secret stored in environment variables
api_url = "https://api.kraken.com"
apikey = vault_Client.get_secret('kraken', 'KRAKEN_API_KEY')
secret = vault_Client.get_secret('kraken', 'KRAKEN_API_SECRET')

# Attaches auth headers and returns results of a POST request
def kraken_request(uri_path, data, api_key, api_sec):
    headers = {}
    headers['API-Key'] = api_key
    # get_kraken_signature() as defined in the 'Authentication' section
    headers['API-Sign'] = get_kraken_signature(uri_path, data, api_sec)
    req = requests.post((api_url + uri_path), headers=headers, data=data)
    return req

# Construct the request and print the result

def get_address(asset, method):
    new = 0
    def get():
        res = kraken_request('/0/private/DepositAddresses', {
            "nonce": str(int(1000 * time.time())),
            "asset": asset,
            "method": method,
            "new": new
        }, apikey, secret)
        print(res.json())
        return res.json()
    res = get()
    if res:
        if len(res['error']) < 1:
            for adr in res['result']:
                try:
                    check = adr['new']
                    address = adr['address']
                    return address
                except KeyError:
                    pass
            new = 1
            res2 = get()
            if len(res2['error']) > 0:
                return address
            else:
                for adr in res2['result']:
                    if adr['new']:
                        address = adr['address']
                        return address
        else:
            return res['error']


# spec = {
#     'USDT':{'name':'USDT','method': 'Tether USD (TRC20)'},
#     'BTC':{'name':'XBT','method': 'Bitcoin'},
#     'ETH':{'name':'ETH', 'method': 'Ethereum (ERC20)'},
#     'BCH':{'name':'BCH', 'method': 'Bitcoin Cash'},
# 'DASH':{'name':'DASH', 'method': 'Dash'},
# 'XMR':{'name':'XMR', 'method': 'Monero'},
# 'LTC':{'name':'LTC', 'method': 'Litecoin'},
# 'SOL':{'name':'SOL', 'method': 'Solana'},
#
# }
#
# adres = get_address('SOL', 'Solana')
# print(adres)
# resp = requests.get('https://api.kraken.com/0/public/Assets')

# print(resp.json()['result'])
# print(list(resp.json()['result'].keys())[15])
# print(resp.json()['result'].values())
# i = -1
# for value in resp.json()['result'].values():
#     i += 1
    # if value['altname'] == 'XBT':
    #     print(list(resp.json()['result'].keys())[i])
        # print(value['altname'])

        # for key in list(resp.json()['result']):
        #
        #     print(key.index)
# print(resp.json()['result'].keys().resp.json()['result'].values())
