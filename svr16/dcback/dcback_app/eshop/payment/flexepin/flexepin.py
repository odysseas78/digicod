import hashlib
import hmac
import json
import math
from pprint import pprint
import requests
import time, os, sys
sys.path.insert(0, '/home/dcback')
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from eshop.models import Jsonfile
from django.conf import settings



class Flexepin:

    def __init__(self, test=False):
        setting=Jsonfile.objects.filter(name='Shopsettings').first().json
        if test or setting.get('Other').get('TestModus'):
            key = settings.ENV_DICT.FLEXEPIN_TEST_KEY.encode()
            secret = settings.ENV_DICT.FLEXEPIN_TEST_SEC.encode()
            rootPath = "https://testrest.flexepin.com"
            # print(key)
            # print(secret)
        else:
            key = settings.ENV_DICT.FLEXEPIN_KEY.encode()
            secret = settings.ENV_DICT.FLEXEPIN_SEC.encode()
            rootPath = "https://rest.flexepin.com"
        
        if key and secret:
            self.key = key
            self.secret = secret
            self.rootPath = rootPath
            # print(self.key)
            # print(self.secret)
            # print(self.rootPath)
        else:
            raise RuntimeError('NO KEY/SECRET')
        
    def random_code(self, length=16, low=True, up=True, num=True, spchr=True):
        import secrets
        lower = "abcdefghijklnopqrstuvwxyz"
        uper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        number = "1234567890"
        spchar = "+-/*!&$#?=@<>"
        chars = ""
        if low == True:
            chars += lower
        if up == True:
            chars += uper
        if num == True:
            chars += number
        if spchr == True:
            chars += spchar
        return ''.join([secrets.choice(chars) for i in range(length)])

    def microtime(self, get_as_float=False):
        if get_as_float:
            return time.time()
        else:
            return '%f %d' % math.modf(time.time())

    def do_private_query(self, requestMethod, requestUri, body=None):
        '''
        do_private_query('GET', 'status', None)\n
        do_private_query('GET', 'voucher/validate/{0}/{1}/{2}'.format(pin, terminalId, transId), None)\n
        do_private_query('PUT', 'voucher/redeem/{0}/{1}/{2}'.format(pin, terminalId, transId), {"customer_ip":"192.168.0.1"})
        '''
        requestUri = '/{0}'.format(requestUri)
        url = '{0}{1}'.format(self.rootPath, requestUri)
        mt = self.microtime().split(' ')
        nonce = '{0}{1}'.format(mt[1], mt[0][2:6])

        thejson = None
        if body:
            thejson = json.dumps(body,separators=(',',':'))

        payload = ''
        payload = '{0}{1}\n'.format(payload, requestMethod)
        payload = '{0}{1}\n'.format(payload, requestUri)
        payload = '{0}{1}\n'.format(payload, nonce)
        if thejson:
            payload = '{0}{1}'.format(payload, thejson)
        #print(payload)

        signature = self.get_signature(payload)
        #print(signature)

        headers = {'content-type': 'application/x-www-form-urlencoded',
                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': '/',
                   'Connection': 'keep-alive',
                   'AUTHENTICATION': 'HMAC {0}:{1}:{2}'.format(self.key.decode(), signature, nonce)
                   }
        if requestMethod == 'PUT':
            return requests.put(url, data=thejson, headers=headers)
        elif requestMethod == 'POST':
            return requests.post(url, data=thejson, headers=headers)
        elif requestMethod == 'GET':
            print(url)
            print(headers)
            return requests.get(url, headers=headers)

    def get_signature(self, payload):
        return hmac.new(self.secret, payload.encode(), hashlib.sha256).hexdigest()




fp = Flexepin(test=False)

# print(fp.do_private_query('GET', 'status', None).text)

#print(fp.do_private_query('GET', 'voucher/validate/{0}/{1}/{2}'.format(pin, terminalId, transId), None).text)

#print(fp.do_private_query('PUT', 'voucher/redeem/{0}/{1}/{2}'.format(pin, terminalId, transId), {"customer_ip":"192.168.0.1"}).text)

#print(fp.do_private_query('GET', 'trans/between/2021-08-21/2021-08-21/DIGIDAGLTD249BDZ/'+trId, None).text)
# response = fp.do_private_query('GET', 'trans/between/2021-08-16/2021-08-16/DIGIDAGLTD249BDZ/'+trId, None).json()
# response = fp.do_private_query('GET', 'trans/trans_id/880821/digicod.eu/ksnd7j395kl93874njdk', None).json()
# pprint(response)

# if response['transactions']:
# try:
#     sum = 0
#     for item in response['transactions']:
#         if item['result_description'] == 'Success':
#             print(item)
#             print(f"{item['currency']} - {item['description']} - {item['cost']}")
#             sum += item['cost']
#
#     print(sum)
# except Exception as d:
#     print(d)

#print(random_code(16, False, True, True, False))





