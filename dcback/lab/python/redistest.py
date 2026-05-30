import json
import secrets
import sys
sys.path.insert(0, '/home/dcback')
import django
import asyncio, os, sys
sys.path.insert(0, '/home/dcback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
import pickle
import redis, base64
from eshop.Utilss.utils import save_obj, read_obj, DictObj
from eshop.models import Basket, Order, User
from django.db import models
from time import sleep


# qs = Order.objects.all()
# print(qs)
# dd = pickle.dumps(qs)
# dd64 = base64.decode(dd)
# ggg = 1000
# sss={
#     'ass':{
#         'aa':{
#             'key':'gggggg'
#             },
#         'bb':123456
#         }
#     }

# ss = {'name': {str(ggg):{'Hercules':'Max'}}, 'age': 25}

# obj = DictObj({})
# obj.ass= 65
# obj = obj.to_dict()
# obj.update(ss)
# obj.update(sss)
# obj = DictObj(obj)
# print(obj.to_dict())

# pickle.dumps(obj)
# with open('dddddddd', "br") as f:
#     dd = f.read()

# print(sss.keys())   # Ausgabe: 25

# ll = pickle.loads(bytes(strdd))
# obj = {'o.martasidis@yahoo.de':secrets.token_urlsafe(64)}
# print(obj)
# dd = pickle.dumps(obj)
# r = redis.Redis(host='localhost', port=6379, decode_responses=True)
# g = r.hset(1,'hhhh:123456', mapping={'kkk':64546})
# g = r.scan()
# print(g)
# d = r.delete('Order_all', 'TestModel', 'Order')
# g = r.scan()
# print(len(g))
# g = r.get('Order_all')
# print(pickle.loads(g).get('o.martasidis@yahoo.de'))
# sleep(10)
# g = r.get('Order_all')
# print(g)
# a.save()
# a.zzz = a
# ff = a(json={'gagagaga':'seseseseses'})
# pd = pickle.dumps(a)
# g = r.set('Order', pd)
# pickle.loads(g).filter(id=880001)
# print(r.keys())x
# from djoser.conf import settings
# qs = Basket.objects.get(fingprint='c68b42342f9bddaa6deab0f51517c985f97bb7339faf9aede508ab11f90ab969')
# print(qs)