import os, sys, secrets, string, base64
from secrets import token_bytes
from pickletools import bytes8
from sqlite3 import Binary
from cryptography.fernet import Fernet
sys.path.insert(0, '/home/dcback')
from datetime import datetime, timedelta
from decimal import Decimal
from html import entities
from locale import currency
import subprocess
from tokenize import Number
from unicodedata import decimal
from django.forms.models import model_to_dict
import jsons
import json
from django.db.models import Q
from loguru import logger
from rest_framework import serializers
from lib.PersistentDictObj import PersistentDictObj



import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from eshop.models import *
from django.core import serializers as SeriaLizer
# from eshop.payop.functions import def check_inv_status
from loguru import logger
import secrets
from eshop_api.utils import get_geopos, Verify
# 
import base64
from base64 import b64encode, b64decode
import pickle
import time
import pytz
# from pf2 import find_stocks
# from binance import Client
import requests
from pprint import *
from django.db.models import Count, F, Value, OuterRef, Subquery
from django.db.models.functions import Length, Upper
from django.db.models.lookups import GreaterThan
import redis, time
from pprint import *
from eshop.serializers import WalletOrderSerializer
from eshop.Utilss.utils import DictObj
from rest_framework.response import Response
from collections import OrderedDict
from api.utils.encb64 import encb64
from api.serializers import *
from django.contrib.auth.tokens import default_token_generator
from sesame.utils import get_query_string
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone

User = get_user_model()
from django.conf import settings


# print(timezone.now() - timedelta(minutes=7))
def generate_verification_url(user):
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    # current_site = get_current_site(request)
    # Assumes you have a URL pattern named 'activate'
    # relative_url = reverse("login",kwargs={'uidb64': uid, 'token': token})
    full_url = f'https://current_site.domain.de/login/{token}{uid}'
    return full_url

# dbjsonfile = Jsonfile.objects.filter(name='Shopsettings').first()
# Shopsettings = PersistentDictObj(dbjsonfile=dbjsonfile, dbjsonfileonly=True)

# user = User.objects.filter(username="m.odysseas78@gmail.com").first()
# wallet = CoinWallet.objects.filter(user=user).first()
# amount = 22.98
# Shopsettings.hhh = 25
# x = user.coinwallet.deposit(amount,  "Top-Up with Neosurf", '', {'amount':amount, 'description':'neosurf'})
# x = user.coinwallet.withdraw(amount,  "Payment for order Nr 3975985ert73948", '')



class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # oder str(obj) für eine Zeichenkettenrepräsentation
        # Lassen Sie die Basisklasse den Typenfehler werfen, falls nicht abgefangen
        return super(DecimalEncoder, self).default(obj)



class GetData:
    
    
    def __init__(self, qst, filtr='', fields='__all__'):
        '''Description'''
        self.model = {'GetCategory':'Category', 'GetBrand':'Brand', 'GetProduct':'Product', 'GetCart':'Cart'}

        self.qs = eval(f"{self.model.get(qst)}Serializer.Meta.model.objects.filter({filtr})")
        self.serializers = []
        self.fexec = ''''''
        self.nested = []
        # self.serializer = eval(f'{self.model.get(qst)}Serializer')
        self.fields = []
    def get_keys_from_nested_dict(self, data, level=0):
        # Wenn das aktuelle Datenstück ein Dictionary ist
        fields = []
        if isinstance(data, dict):
            
            for key in data:
                # self.serializers.append(eval(f'{self.model.get(key)}Serializer()'))
                self.nested.append([f'{self.model.get(key)}',f'{self.model.get(key).lower()}={self.model.get(key)}Serializer(many=True)'])
                
                # self.serializers.append(f'{self.ggg(model=self.model.get(key), fields="__all__",nested=)}')
                # serializer = eval(f'{self.model.get(key)}Serializer')
                # Gibt den Schlüssel und seine Ebene zurück
                # self.serializer()[self.model.get(key).lower()] = eval(f'{self.model.get(key)}Serializer(many=True)')
                print("Level", level, ":", key)
                
                # Rekursiver Aufruf, um in den nächsten verschachtelten Dictionary oder Liste zu gehen
                self.get_keys_from_nested_dict(data[key], level + 1)
        # Wenn das aktuelle Datenstück eine Liste ist
        elif isinstance(data, list):
            
            for item in data:
                if isinstance(item, str):
                    fields.append(item)
                    # print(f'{self.key}')
                    # f'{self.model.get(key)}Serializer().Meta.fields='
                    # print(item)
                # Rekursiver Aufruf, um in den nächsten verschachtelten Dictionary oder Liste zu gehen
                
                self.get_keys_from_nested_dict(item, level)
            self.fields.append(fields)
            
    def ggg(self, model, fields, nested):       
        return f'''class {model}Serializer(serializers.ModelSerializer):
            {nested}

            class Meta:
                model = {model}
                fields = "{fields}"'''
           
        
        
    def getqs(self):
        
        qs = self.model.objects.filter('filtr')
        self.get_keys_from_nested_dict(qs, level=0)
        self.nested.reverse()
        # pprint(self.nested)
        fields = self.fields.copy()
        
        for item in fields:
            pprint(self.fields.index(item))
            
            nestd = ''''''
            mdl = self.nested[self.fields.index(item)]
            # pprint(mdl)
            
            for n in self.nested:
                # nstd = self.nested[self.fields.index(item)]
                if n[0].lower() in item:
                    nestd += f'{n[1]}\n'
            self.serializers.append(self.ggg(model=mdl[0], fields=item, nested=nestd))
        # pprint(self.serializers)
        # print(f'{self.nested}')
        # self.fields.reverse()
        # print(f'{self.fields}')
        # print(f'{self.serializers}')
        # for e in self.serializers:
        #     self.fexec += f'{str(e)+str(self.fields[self.serializers.index(e)])}\n'
        # print(f'{self.fexec}')
        # exec(self.fexec)
        # srz = self.serializer(self.qs, many=True)
        # json_data = json.dumps(srz.data)
        # dd = encb64(json_data, 'encode')
        # return encb64(dd, 'decode')



from redis import Redis
from rq.job import Job
from rq import Queue
# from lab.test import my_slow_function

# Verbindung zu Redis herstellen und Warteschlange erstellen
# q = Queue(connection=Redis())

# Aufgabe in die Warteschlange stellen
# result = q.enqueue(my_slow_function, 50)
# print(result)
# r = redis.Redis(host='localhost', port=6379, db=0)
# r.get('Job')
# job = Job.fetch('my_job_id', connection=redis)
# print(q.get_jobs())
# for job in q.get_jobs():
#     print(job)
#     job.delete()
# the `*` means that redis generates and event id automatically
# r.set('dfg', json.dumps({'jsondata':'uiyiuyiuy'}))
# r.delete('dfg')
# g = r.get('dfg')
# pprint(g)
# time.sleep(3)
# g = r.get('dfg')
# print(g)

# time.sleep(3)
# g = r.get('dfg')
# print(g)

# time.sleep(3)
# g = r.get('dfg')
# print(g)

# time.sleep(3)
# g = r.get('dfg')
# print(g)



# pprint(dd)
# for obj in objects:
#     # Zugriff auf das eigentliche Objekt
#     actual_object = obj.object
#     # actual_object.hh=25
#     # actual_object.aaaa=2555555
#     actual_object.save()
#     print(actual_object.currency)
# d = Currency.objects.all()

# for f in d:
#     print(f.histori)

# f.reverse()
# filtred = filter(lambda x: x.sort(), f)

# d.reverse()
# d.append({'date':datetime.now(), 'price':1.568789})


# cur.histori=None
# cur.save()

# d = pickle.dumps([])
# print(d)
# basket = Currency.objects.all().last()

# pprint(pickle.loads(basket.histori))
# user = Customer.objects.get(user__id=97)
# basket.owner=user
# basket.save()
# def OrderSet():
    
#     order = Orders(
#         basket=basket
#     )
#     order.save()
#     basket.order=order
#     basket.save()
#     order.save()
#     return order

# pprint(OrderSet())

# order = Orders.objects.all().first()
# # order.save()
# pprint(order)
# total_price = sum([product.price * qs.basket_products.get(str(product.id)) for product in qs.products.all()])
# print(qs.save(data={'add':{'id':'2437','value':3}}))
# print((qs.payment_method._meta.model.objects.filter(id=5)))
# print((100-qs.payment_method.fee_rate))
# print((total_price - qs.wallet_payment + qs.payment_method.fee_fix) / (100-qs.payment_method.fee_rate))
# r = redis.Redis(host='localhost', port=6379, decode_responses=False)
# r.json.set('doc', '$', 'data')
# doc = r.json().get('doc', '$')
# dog = r.json().get('doc', '$.dog')
# scientific_name = r.json().get('doc', '$..scientific-name')
# r.set('kuku',kkk)
# pprint(scientific_name)




# True

# 


# pprint(r.hgetall('carts'))




# class RedisCart():
    
#     def getsetId():
#         old=int(r.hget('ids','carts'))
#         new=old+1
#         r.hset('ids','carts',new)
#         return new
    
#     h = r.hset('carts', mapping={
#     'id':getsetId(),
#     'currency': 1,
#     'deleted': 0,
#     'ex_rate': 0,
#     'final_price': 0,
#     'fingprint': 0,
#     'for_anonymous_user': 0,
#     'in_order': 0,
#     'order': 0,
#     'order_final_price': 0,
#     'owner': 0,
#     'payment_method': 3,
#     'payment_method_payment': 0,
#     'payoption': 0,
#     'process_fee': 0,
#     'refund_amount': 0,
#     'total_products': 0,
#     'wallet_payment': 0
#     })
    
    
# r = redis.Redis(
#     host='127.0.0.1',
#     port=6666,
#     decode_responses=True # <-- this will ensure that binary data is decoded
# )

# while True:
#     message = input("Enter the message you want to send to soilders: ")

#     r.publish("events", message)

