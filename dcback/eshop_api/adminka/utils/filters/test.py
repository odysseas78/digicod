import django, os
os.environ['PYTHONPATH'] = '/home/user/.cache/pypoetry/virtualenvs/dcback-po_-vPs_-py3.10/bin/python:$PWD'
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

django.setup()


from django.db.models import Q, F
from django.db.models import Count, F, Value, OuterRef, Sum
from django.db.models.functions import Length, Upper
from django.db.models.lookups import GreaterThan
from django.core import serializers as SeriaLizer
from rest_framework import serializers
import re
from pprint import *
from pathlib import Path
from pickletools import bytes8
from sqlite3 import Binary
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from decimal import Decimal
from html import entities
from locale import currency
import subprocess
from tokenize import Number
from unicodedata import decimal
import jsons
import json
import sys
# print(sys.path)
# sys.path.append("/home/dcback/eshop")
from loguru import logger
# from eshop.utils import read_obj, DictObj, save_obj, check_process_order, json_read, json_save
from eshop.models import Currency, Order, WalletOrder, Cart, CartProduct, Wallet, \
    Customer, Payment, User, Limit, Verification, Jsonfile
# from eshop.payop.functions import def check_inv_status
# from eshop.utils import limitcheck
# import secrets
# from eshop_api.utils import get_geopos, Verify
# from aws import rekognition_objects
import base64
from base64 import b64encode, b64decode
import pickle
import time
import pytz
# from eshop.utils import wolimitcheck
# from binance import Client
import requests
from pprint import *



# fil = [["customer.user.username","contains","noda"],"and",[["pay_amount.dddd","<",20],"or",["pay_currency.shortname","=","CAD"],"or",[["status.kkk","contains","ddd"],"or",["!",["id.kdkdk","<>",123]]]]]
# f1 = '[[{"selector":"user.id","summaryType":"count"}]]'
# # q_obj = Q([Q([Q(['europrice__lt', 27]) & Q(['europrice__gt', 27])]) | Q([Q(['id__gt',27]) & Q(['status', 'completed'])]) | Q(['created_at__gt', '2020-01-01'])])


# selector = '[["created_at.sdafsd",">=","2022-07-30T18:48:00.000Z"],"and",["customer.user.username","=","Abou123"]],"or",["!",["invoice.ttzurtzutu","=",null],"and",["customer.user.username","=","djifanou.gzh"]]'
# flt = '[["europrice","<",20],"and",["pay_currency.shortname","contains","AUD"]"or"["!",[["status.fasdfdfd","=",null],"or",["status","=",""]]]]'
# fltr = '[["europrice","<",20],"and",["pay_currency.shortname","contains","AUD"],"and",[["status","<>",null],"and",["status","<>",""]]],"and",["!", [["status","=",null],"or",["status","=",""]]]'

# # selector2 = re.sub(r'\[.*?\.(.*?),', r'[\1-', selector)


# import re

# def replace_symbol_between_brackets(string, symbol, replacement):
#     pattern = rf'\[.*?{symbol}.*?,\s*'
#     return re.sub(pattern, lambda match: match.group().replace(symbol, replacement), string)

# string = '[["created_at",">=","2022-07-30T18:48:00.000Z"],"and",["customer.user.username","=","Abou123"]],"or",["!",["invoice","=",null],"and",["customer.user.username","=","djifanou"]]'
# new_string = replace_symbol_between_brackets(f1, '.', '__')
# print(new_string)




# start = 0
# fund = 0 
# stop = 0
# cunt = 0
# for b in flt:
    
#     if b == '[':
#         start = 1
#     if start == 1:
#         if b == '.':
#             fund = 1
            
#     elif b == '.':
#         cunt += 1

# def grup_constructor(sel, qs):
#     from django.db.models import Count, Sum
#     dta = []
#     #--------------------------------------------------------------------------
#     def func1(i, kj, vls, cnt):
#         second = (qs.filter(Q([kj, i.get(kj)])).values(*vls).annotate(*cnt, sume=Sum('europrice'))
#                 .order_by('sume')
#                 )
#         f = {'key': i[kj], 'count':i[kj+'__count'], 'items':None, 'summary':[i.get('sume'), i.get(kj+'__count')]}
#         # print(vls)
#         for sec in second:
#             # Orders2ViewSet.info(f'sec | {sec}')
#             f1 = {'key': sec[vls[0]], 'count':sec[vls[0]+'__count'], 'items':None, 'summary':[sec.get('sume'), sec.get(vls[0]+'__count')]}
#             if f.get('items') == None:
#                 f['items'] = []
#             f.get('items').append(f1)
#         return f
#     #--------------------------------------------------------------------------

#     data = []
#     cnt = []
#     vls = []
#     # sel.reverse()
#     for sl in sel:
#         kj = sl.get('selector').replace('.','__').replace('[0]','')
#         # print(kj)
#         cnt.append(Count(kj))
#         vls.append(kj)
#     grup = qs.values(*vls).annotate(*cnt, sume=Sum('europrice')).order_by()
#     return grup, vls
#     for sl in sel:
#         kj = sl.get('selector').replace('.','__').replace('[0]','')
#         # if len(sel)-1 > sel.index(sl):
#         #     sl1 = sel[sel.index(sl)+1]
#         #     kj1 = sl1.get('selector').replace('.','__').replace('[0]','')
#         # Orders2ViewSet.info(f'kj) | {kj} | kj1 {kj1}')
#         first = qs.values(kj).annotate(Count(kj), sume=Sum('europrice')).order_by()
#         # if sel.index(sl) < 1 and len(sel)-1 > 0:
#         #     continue
#         cnt.remove(Count(kj))
#         vls.remove(kj)
#         for i in first:
#             # Orders2ViewSet.info(f'len(vls), len(sel) | {len(vls)} | {len(sel)}')
#             if len(vls) > 0 and len(sel) > 0:
#                 data.append(func1(i,kj,vls,cnt))
#             else:
#                 f = {'key': i[kj], 'count':i[kj+'__count'], 'items':None, 'summary':[i.get('sume'), i.get(kj+'__count')]}
#                 data.append(f)
#     return data

sel = [{"selector":"customer.user.username","desc":False,"isExpanded":True}]
sel2 = [{"selector":"status","desc":False,"isExpanded":True},{"selector":"pay_currency__shortname","desc":False,"isExpanded":False}]

qs = Order.objects.all()

data = {
            "key": "CACTU",
            "items": None,
            "count": 2,
            "summary": [
                3.17,
                2
            ]
        }

{
    "data": [
        {
            "key": "Argentina",
            "items": [
                {
                    "key": 1,
                    "items": [
                        {
                            "key": "CACTU",
                            "items": None,
                            "count": 2,
                            "summary": [
                                3.17,
                                2
                            ]
                        }
                    ],
                    "summary": [
                        131.97,
                        5
                    ]
                }
            ],
            "summary": [
                598.58,
                16
            ]
        }
    ]
}

# # pprint(grup_constructor(sel, qs))
# grup = grup_constructor(sel, qs)[0]
# vls = grup_constructor(sel, qs)[1]
# custom = sel[0].get('selector').replace('.','__').replace('[0]','')
# pay_cur = sel[1].get('selector').replace('.','__').replace('[0]','')
# status = sel[2].get('selector').replace('.','__').replace('[0]','')

# custom_count = sel[2].get('selector').replace('.','__').replace('[0]','')+'__count'
# grp = grup.values(status).annotate(Count(status), Sum('europrice')).filter(Q([pay_cur, 'BTC']))
# pprint(grp)
# pprint()
# for t in grup:
#     if t.get(vls[0]) == 'coulbyissabc':
#         print(t)
#---------------------------

#----------------------------  


# def grup_constructor(sel, qs):
#     from django.db.models import Count, Sum
#     res = []
#     cnt = []
#     vls = []
#     # sel.reverse()
#     for sl in sel:
#         kj = sl.get('selector').replace('.','__').replace('[0]','')
#         # print(kj)
#         cnt.append(Count(kj))
#         vls.append(kj)
#     if request.query_params.get('totalSummary') and len(json.loads(request.query_params.get('totalSummary'))) > 0:
#         totalsumsel = json.loads(request.query_params.get('totalSummary'))[0].get("selector")
#         summary = qs.values('europrice').aggregate(sume=Sum(totalsumsel)).get('sume')
#     else:
#         summary = ''
    
#     if request.query_params.get('groupSummary') and len(json.loads(request.query_params.get('groupSummary'))) > 0:
#         grupsumsel = json.loads(request.query_params.get('groupSummary'))[0].get("selector")
#         annon = [Sum(grupsumsel)]
#     else:
#         annon = None
#     grup = qs.values(*vls).annotate(*cnt, sume=Sum(grupsumsel)).order_by()
    
#     for i in grup.values(key=F(vls[0])).annotate(count=Count(vls[0]), *annon[0]):
#         q_obj = []
#         i['items']=None
#         i["summary"] = [i.get('summary'),i.get('count')]
#         if len(vls) > 1:
#             i['items']=[]
#             i.pop('count')
#             q_obj.append(Q([vls[0], i.get('key')]))
#             for i1 in grup.values(key=F(vls[1])).annotate(count=Count(vls[1]), *annon[0]).filter(*q_obj):
#                 i1['items']=None
#                 i1["summary"] = [i1.get('summary'),i1.get('count')]
#                 i['items'].append(i1)
#                 if len(vls) > 2:
#                     i1['items']=[]
#                     i1.pop('count')
#                     q_obj.append(Q([vls[1], i1.get('key')]))
#                     for i2 in grup.values(key=F(vls[2])).annotate(count=Count(vls[2]), *annon[0]).filter(*q_obj):
#                         i2['items']=None
#                         i2["summary"] = [i2.get('summary'),i2.get('count')]
#                         i1['items'].append(i2)
#                         if len(vls) > 3:
#                             i2['items']=[]
#                             i2.pop('count')
#                             q_obj.append(Q([vls[2], i2.get('key')]))
#                             for i3 in grup.values(key=F(vls[3])).annotate(count=Count(vls[3]), summary=Sum(grupsumsel)).filter(*q_obj):
#                                 i3['items']=None
#                                 i3["summary"] = [i3.get('summary'),i3.get('count')]
#                                 i2['items'].append(i3)
#                                 if len(vls) > 4:
#                                     i3['items']=[]
#                                     i3.pop('count')
#                                     q_obj.append(Q([vls[3], i3.get('key')]))
#                                     for i4 in grup.values(key=F(vls[4])).annotate(count=Count(vls[4]), summary=Sum(grupsumsel)).filter(*q_obj):
#                                         i4['items']=None
#                                         i4["summary"] = [i4.get('summary'),i4.get('count')]
#                                         i3['items'].append(i3)
#                                         if len(vls) > 5:
#                                             i4['items']=[]
#                                             i4.pop('count')
#                                             q_obj.append(Q([vls[4], i4.get('key')]))
#                                             for i5 in grup.values(key=F(vls[5])).annotate(count=Count(vls[5]), summary=Sum(grupsumsel)).filter(*q_obj):
#                                                 i5['items']=None
#                                                 i5["summary"] = [i5.get('summary'),i5.get('count')]
#                                                 i4['items'].append(i5)
#         res.append(i)
#     return [res, [summary]]

# vls.reverse()
# grup_constructor(sel2, qs)
# pprint(grup_constructor(sel2, qs))
