from functools import reduce
import itertools
from shlex import join
import io, sys
import redis.utils
sys.path.insert(0, '/home/dcback')
from operator import setitem
from pickletools import bytes8
from sqlite3 import Binary
import time
from cryptography.fernet import Fernet
from datetime import datetime, timedelta, date, timezone
from decimal import Decimal, ROUND_HALF_UP
from html import entities
from locale import currency
from time import sleep, strftime
from tokenize import Number
from unicodedata import decimal
# from coreapi import Object
# import jsons
import json
from django.db.models import Q, OuterRef, Subquery
from datetime import datetime, timedelta
from loguru import logger
from rest_framework import serializers
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from eshop_api.cart.serializers import CartSerializer
# from eshop.PrepaidForge.Order import get_orders
from django.core import serializers as SeriaLizer
# from eshop.payop.functions import def check_inv_status
from loguru import logger
import secrets
from eshop_api.utils import get_geopos, Verify
from eshop_api.adminka.utils.utils import construct
from eshop.Utilss.utils import read_obj, save_obj, DictObj
import base64
from base64 import b64encode, b64decode, decode
from rest_framework.authtoken.models import Token
# from pf2 import find_stocks
from pprint import pprint
import requests
import pdfkit
from eshop.order_email_send import orderemail
import json
from django.core.serializers.json import DjangoJSONEncoder
import operator
# from django.db.models import Avg, Count, Min, Sum
# from eshop.kinguin.order import check, get_keys
from binance import Client
import decimal
import pickle
from time import sleep, perf_counter
# print((datetime.now() + timedelta(hours=24)).timestamp())

from eshop.payment.utils_payment import BlList
from rest_framework import serializers
from djoser.utils import *
from django.db.models import Q,F, Value
from django.http import JsonResponse
from django.core.serializers import serialize
import json
import logging
from rest_framework.authtoken.models import Token
from django.core import serializers as SeriaLizer
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from djoser.utils import login_user, logout_user, settings
# from apps.shop.services import *
from lib.utils.getDatafile import GetDatafile

# from eshop.models import Payment
from apps.accounts.models import Customer as Customer2
from apps.shop.models import CartProduct, Product, Cart, Brand, Payment as Payment2
# User = get_user_model()
product_id = 3330
pqs = Product.objects.get(id=3330)

# cpqs = CartProduct.objects.filter(product__id=3330)
# cpqs.delete()
# cqs = Cart.objects.get(id=58)
# print(cqs.fingprint.fingprint)
# cproduct, created = CartProduct.objects.get_or_create(
#     product=pqs,
#     cart=cqs,
#     defaults={
#         "qty":3
#     }
# )
# if created:
#     cqs.products.add(cproduct)
#     cqs.save()
# else:
#     cproduct.qty = 0
#     if cproduct.qty == 0:
#         cproduct.delete()
#     # cproduct.save()
#     cqs.save()
# cartprod = CartProduct.objects.create(cart=cqs, product=pqs)

# print(cpqs)
# print(cqs.products.all())

# fields3 = {
    
#         field2.user.username
#     for field2 in Customer2.objects.all()
#     # if field.name != "id"
# }
# cqs = Cart.objects.get(id=7)
# pqs = Brand.objects.filter(title="Zalando").first().brand_products.all()
# g = pqs.first().regions

# regs = list({
#     region
#     for product in pqs
#     for region in json.loads(product.regions)
# })

# pqs.price = Decimal(pqs.supplier_product.get("stock").get("purchasePrice"))
# pqs.save()
# pqs.save()
# qs = CartProduct.objects.all().first()
# cqs.products.add(pqs)

# qs.save()
# r = CartProduct(cart=cqs, title=pqs.title, item_price=pqs.price, product=pqs, qty=1)

# r.save()
# cqs.products.add(r)
# cqs.delete()
# qs.delete()
# qs.save()
# print(regs)

# for p in qs:

#     obj = Payment2.objects.create(
#         type = p.type,
#         provider = p.provider,
#         name = p.name,
#         # payoptions = p.payoptions,
#         # currencies = p.currencies,
#         # brands = p.brands,
#         enabled = p.enabled,
#         desc = p.desc,
#         fee_rate = p.fee_rate,
#         fee_fix = p.fee_fix,
#         image = p.image,
#         image2 = p.image2,
#         svg = p.svg,
#         html = p.html,
#         json = p.json,
#         deleted = p.deleted

#         )
   
#     obj.payoptions.set(p.payoptions.all())
#     obj.currencies.set(p.currencies.all())
#     obj.brands.set(p.brands.all())
#     dd.currencies.set(p.currencies.all())
#     dd.brands.set(p.brands.all())
    # dd.save()

# Customer2.objects.bulk_create(rows)

# User = get_user_model()
# qs = Basket.objects.filter(id=179).first()
# user = User.objects.filter(id=97).first()
# jsn = SeriaLizer.serialize('json', [qs])
# [product.price * int(self.basket_products.get(str(product.id)).get('qty')) for product in self.products.all()]
# token = CustomToken.objects.filter(key='c6396093ebe8525eb499f801b891c76cedfe4931')
# auth_token = login_user(request=self.request, user=user).key
# print(qs)


logger = logging.getLogger(__name__)
# def factorial(x):
#     if x == 0:
#         return 1
#     return x * factorial(x-1)

# def fib(n):
#     if n in (1,2):
#         return 1
#     return fib(n-1) + fib(n-2)

# def simple(n):
#     lst = []
#     k = 0
#     for i in range(2, n+1):
#         for j in range(2, i):
#             if i % j == 0:
#                 k += 1
#         if k == 0:
#             lst.append(i)
#         else:
#             k = 0
#     return lst





# Beispiel verwenden
# file_path = "/home/dcback/lab/MyDB"
# df = PersistentDictObj(file_path)

# # Neues Attribut hinzufügen
# df.malakies = 457896 #/
# df.kufala = 'shades' #?
# df.kuku = 124
# df.lolo = 'malakies'

# pprint(df.dcsettings.test)  # Ausgabe: neuer Wert

# Attribut löschen
# del df.neuer_key

# Versuch, das gelöschte Attribut zu lesen
# try:
#     print(df.neuer_key)
# except AttributeError as e:
#     print(e)  # Ausgabe: 'PersistentDictObj' object has no attribute 'neuer_key'



# from datetime import date

# class Employee:
#     def __init__(self, name, birth_date):
#         self.name = name
#         self.birth_date = birth_date

#     @property
#     def name(self):
#         return self._name

#     @name.setter
#     def name(self, value):
#         self._name = value.upper()

#     @property
#     def birth_date(self):
#         return self._birth_date

#     @birth_date.setter
#     def birth_date(self, value):
#         self._birth_date = date.fromisoformat(value)
        
#     def ff(self, hh):
#         return 

from asgiref.sync import async_to_sync
from http.cookies import SimpleCookie

# connection = get_redis_connection('default')
# connection.publish("event", 'message vrom default')

# connection = get_redis_connection('channels')
# connection.publish("event", 'message from channels')


import asyncio, json
import redis









class myRedis(redis.Redis):
    
    def __init__(self, **kwargs):
        kw = DictObj({**kwargs})
        self.kk = DictObj({})
        self._kk = self.kk.to_dict()
        super().__init__(**kw.to_dict())
        
    def dsset(self,data):
        r = self
        r.hset('hh',mapping=ff)
        t = r.hgetall('hh')
        return r.hset
    
    @property
    def dget(self):
        return self._kk
    
    @property
    def dset(self):
        print(self.kk.to_dict())
        return self.kk

    # @dget.getter
    # def dset(self, value):
    #     self._dget = value.upper()

b = {'kukla': '456', 'uuuu': 'ooooo', 'hhh': '456', 'zzz': 'ooooo', 'hhshhh': '456', 'usuuu': {'kukla':'789456123'}, 'malakies': '456'}
inventory_json = {
    "inventory": {
        "mountain_bikes": [
            {
                "id": "bike:1",
                "model": "Phoebe",
                "description": "This is a mid-travel trail slayer that is a fantastic "
                "daily driver or one bike quiver. The Shimano Claris 8-speed groupset "
                "gives plenty of gear range to tackle hills and there\u2019s room for "
                "mudguards and a rack too.  This is the bike for the rider who wants "
                "trail manners with low fuss ownership.",
                "price": 1920,
                "specs": {"material": "carbon", "weight": 13.1},
                "colors": ["black", "silver"],
            },
            {
                "id": "bike:2",
                "model": "Quaoar",
                "description": "Redesigned for the 2020 model year, this bike "
                "impressed our testers and is the best all-around trail bike we've "
                "ever tested. The Shimano gear system effectively does away with an "
                "external cassette, so is super low maintenance in terms of wear "
                "and tear. All in all it's an impressive package for the price, "
                "making it very competitive.",
                "price": 2072,
                "specs": {"material": "aluminium", "weight": 7.9},
                "colors": ["black", "white"],
            },
            {
                "id": "bike:3",
                "model": "Weywot",
                "description": "This bike gives kids aged six years and older "
                "a durable and uberlight mountain bike for their first experience "
                "on tracks and easy cruising through forests and fields. A set of "
                "powerful Shimano hydraulic disc brakes provide ample stopping "
                "ability. If you're after a budget option, this is one of the best "
                "bikes you could get.",
                "price": 3264,
                "specs": {"material": "alloy", "weight": 13.8},
            },
        ],
        "commuter_bikes": [
            {
                "id": "bike:4",
                "model": "Salacia",
                "description": "This bike is a great option for anyone who just "
                "wants a bike to get about on With a slick-shifting Claris gears "
                "from Shimano\u2019s, this is a bike which doesn\u2019t break the "
                "bank and delivers craved performance.  It\u2019s for the rider "
                "who wants both efficiency and capability.",
                "price": 1475,
                "specs": {"material": "aluminium", "weight": 16.6},
                "colors": ["black", "silver"],
            },
            {
                "id": "bike:5",
                "model": "Mimas",
                "description": "A real joy to ride, this bike got very high "
                "scores in last years Bike of the year report. The carefully "
                "crafted 50-34 tooth chainset and 11-32 tooth cassette give an "
                "easy-on-the-legs bottom gear for climbing, and the high-quality "
                "Vittoria Zaffiro tires give balance and grip.It includes "
                "a low-step frame , our memory foam seat, bump-resistant shocks and "
                "conveniently placed thumb throttle. Put it all together and you "
                "get a bike that helps redefine what can be done for this price.",
                "price": 3941,
                "specs": {"material": "alloy", "weight": 11.6},
            },
        ],
    }
}

# r = myRedis(host="localhost", port=6379, db=0)

# r = redis.Redis(host="localhost", port=6379, db=0)
# res2 = r.scan()
# print(res2)
# gg = r.hgetall('hh')
# gg['malakies'] = 456
# r.lpush('onlineusers','kkkkkkk222',4562222)
# res1 = r.json().set("bikes:inventory", "$", inventory_json)

# print(r.json().set("ONLINEUSERS","$.hhh.dedede",[88888, 99999, 77777, 66666, 55555, 44444, 33333, 22222, 11111, 00000]))
# pprint(r.json().get("ONLINEUSERS"))

# r.dget


import pickle
import os

# Beispiel verwenden
# file_path = "/home/dcback/lab/MyDB"
# df = PersistentDictObj(file_path)









# foo_cookie = cookies['foo']

# assert foo_cookie.value == 'bar'
# assert foo_cookie['domain'] == 'example.com'
# assert foo_cookie['path'] == '/some/path'
# assert not foo_cookie['expires']

# baz_cookie = cookies['baz']
# assert baz_cookie.value == '42'
# assert baz_cookie['expires'] == 'Thu, 12-Jan-2017 13:55:08 GMT'


# Extra: an example of parsing Flask's response cookies:
# with app.test_client() as c:
#     rv = c.get('/?vodka=42')
#     cookies = SimpleCookie('\r\n'.join(rv.headers.get_all('Set-Cookie')))
# print(COOKIES(cooc.get('Cookie')).get('_polz'))
# print(f'''
#       {df.basket.total_price}
#       {df.basket.total_products}
#       {df.basket.basket_products}
#       {df.basket.products}
#       ''')
# d = df.to_dict()
# ss = {
#     'basket':{'total_price':d.get('basket').get('total_price'), 'total_products':d.get('basket').get('total_products'), \
#         'basket_products':d.get('basket').get('basket_products'), 'products':d.get('basket').get('products')}
# }
# # b64 = base64.b64encode(json.dumps(df.to_dict().get('basket'),cls=DecimalEncoder).encode()).decode()
# # pprint(b64)




# secr = 'JTIyJTFEJTBBJTE2JTEwJTE3JTA0JTA3JTVDJTVE'
# gggg = 'Ih0KFhAXBAdcXQ=='
# bstr = 'Odysseas78'
# key='mysecretkey'

# # # print(base64.b64encode(secr.encode()).decode())

# # print(urlsafe_base64_decode(secr).decode())
# print(urlsafe_base64_encode(gggg.encode()))
# b64 = encrypt(json.dumps(ss))
# pprint(decrypt('KhwHJwIBDhEf'))
# a = encrypt(json.dumps({'GetBasket':{'addproduct':1, 'qty':1}}))
# pprint(a)
# b = json.loads(decrypt(a))
# pprint(type(b))

# qs = Brand.objects.filter(wsaler='Prepaidforge')

# s = [p for p in qs if p.products]
# print(s)

# print(qs.first().products.filter(qty=0).count())
