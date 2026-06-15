import os, sys, django, requests
sys.path.insert(0, '/home/dcback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from pprint import pprint
import json, jsons
# from eshop.utils import save_obj, read_obj, listUniq
from flexepin import Flexepin
from eshop.productorder.prodOrder import ProdOrder
# from rest_framework.authtoken.models import Token

# tokens = Token.objects.all()
# tokens.delete()

from eshop.models import Order

# res = requests.post('https://odys.digicod.eu/api/gate/',{'malakies':123456789})

# fp = Flexepin()
# order = Order.objects.all().first()

# print(order)
# pin = '5803219255596627'
# terminalId = 'digicod.eu'
# po = ProdOrder(order)
# res = po.do_prod_order()
# print(res)
# transId = fp.random_code(length=16, low=False, spchr=False)

# print(trId)
# pprint(fp.do_private_query('GET', 'status', None).json())
# pprint(fp.do_private_query('GET', 'voucher/validate/{0}/{1}/{2}'.format(pin, terminalId, transId), None).json())
# pprint(fp.do_private_query('PUT', 'voucher/redeem/{0}/{1}/{2}'.format(pin, terminalId, transId), {"customer_ip":"192.168.0.1"}).json())

# setting=Jsonfile.objects.filter(name='Shopsettings').first().json

# pprint(setting)

res = {'cost': 19.21,
 'currency': 'CAD',
 'description': 'Flexepin CAD 20',
 'ean': '9350233002076',
 'result': '0',
 'result_description': 'Success',
 'serial': '53001000578757699',
 'status': 'ACTIVE',
 'trans_no': '213719448',
 'transaction_id': 'MN02QL1YOOIG24W7',
 'value': 20}

res2 = {
    "result": "4075",
    "result_description": "Voucher is not found",
    "transaction_id": "4AJZLHIATAEIVNCC",
    "trans_no": "9397484"
}

keys = ['cost','ean','serial','trans_no','transaction_id']

# for key in keys:
#     try:
#         del res2[key]
#     except:
#         continue

# pprint(res2)