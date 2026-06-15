import sys, os, django, json, time
from decimal import Decimal
from django.db.models import Q
sys.path.insert(0, '/home/dcback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from eshop.models import  ShopSetting, Product, Brand, Category, ProductCodes, Orders
from eshop.PrepaidForge.pf import Pforge
from eshop.payment.neosurf.neosurf_pay import Neosurf



def processOrder(oid):
   ns = Neosurf()
   pf = Pforge()
   orderqs = Orders.objects.filter(uuid=oid).first()
   trx = ns.soap_get_trx_detail('a3d8dda9-fcf8-442f-a4f1-536d712622e9', 'no')
   print(trx)
   if trx.get('status') == 'ok':
      orderqs.status = "processing"
      orderqs.save()
      r = pf.prorder(orderqs)
      return r
   return {'type':'error'}

 

# r = processOrder('a3d8dda9-fcf8-442f-a4f1-536d712622e9')
# print(r)