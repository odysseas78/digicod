import hashlib
import json
import os
from collections import OrderedDict
from pprint import pprint
import django
import jsons
import requests
# from config.settings import env_dict

env_dict = {}
env_dict["PayDo_APP_ID"]="8b01ab3b-df24-4acb-a6e0-2a4526fa1df9"
env_dict['PayDo_JWT']="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ODc5Nzc2LCJ0aW1lIjoxNzE0NDExNDAxLCJ0d29GYWN0b3IiOnsicGFzc2VkIjp0cnVlfSwidG9rZW5JZCI6NDM5LCJleHBpcmVkQXQiOm51bGwsInJvbGUiOjIsImFjY2Vzc1Rva2VuIjoiOTRhNGJmMGUwN2QzZTU5YTBlYmE1OWI1In0.PvoC5fH20pxMn2PlzsUx-1qXSVcugw1FJl1igkBJCrY"
env_dict['PayDo_SECRET']="4822fdbb3bd95cf9e3b3cc64"


def get_paymethod(title=None, identifier=None):
    url = 'https://paydo.com/v1/instrument-settings/payment-methods/available-for-application/'+env_dict.get('PayDo_APP_ID')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer '+env_dict.get('PayDo_JWT')
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
# pprint(get_paymethod())

# with open('payopmethods.json', 'r') as f:
#     gg = f.read()
# dd = jsons.loads(gg).get('data')

# for i in dd:
#     pprint(i.get('paymentMethod').get('title'))