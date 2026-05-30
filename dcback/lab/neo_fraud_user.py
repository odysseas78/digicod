from pickletools import bytes8
from sqlite3 import Binary
from cryptography.fernet import Fernet
from datetime import datetime, timedelta, date
from decimal import Decimal
from html import entities
from locale import currency
import subprocess
from tokenize import Number
from unicodedata import decimal

import jsons
import json
from django.db.models import Q
from loguru import logger
from rest_framework import serializers
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from eshop.Utilss import read_obj, DictObj, save_obj, check_process_order, json_read, json_save
from eshop.models import Currency, Order, WalletOrder, Cart, CartProduct, Wallet, \
    Customer, Payment, User, Limit, Verification, Jsonfile
from django.core import serializers as SeriaLizer
# from eshop.payop.functions import def check_inv_status
from loguru import logger
from eshop.Utilss import limitcheck
import secrets
from eshop_api.utils import get_geopos, Verify
# from aws import rekognition_objects
from apps.accounts.models import *
import base64
from base64 import b64encode, b64decode
import pickle
import time
import pytz
import markdown
from eshop.Utilss import wolimitcheck
# from pf2 import find_stocks
# from binance import Client
import requests
import pdfkit
from eshop.order_email_send import orderemail

# print((datetime.now() + timedelta(hours=24)).timestamp())



def fraud_check():
    with open('neosurf_fraud.txt', 'r') as f:
        r = f.read()
    result = {}
    for i in r.split('\n'):
        worder = WalletOrder.objects.filter(id=i[-6:]).first()
        if worder:
            if worder.owner.user.username not in result:
                ips = LoginStatistic.objects.filter(username=worder.owner.user.username).first()
                result.update({worder.owner.user.username:{
                    'order':[], 'name':worder.owner.user.first_name+' '+worder.owner.user.last_name,
                    'email':worder.owner.user.email, 'ip':ips.ip, 'country':ips.geopos}})
                result[worder.owner.user.username]['order'].append(i[-6:])
            else:
                result[worder.owner.user.username]['order'].append(i[-6:])
        else:
            order = Order.objects.filter(id=i[-6:]).first()
            if order:
                if order.customer.user.username not in result:
                    ips = LoginStatistic.objects.filter(username=order.customer.user.username).first()
                    result.update({order.customer.user.username:{
                        'order':[], 'name':order.customer.user.first_name+' '+order.customer.user.last_name,
                        'email':order.customer.user.email, 'ip':ips.ip, 'country':ips.geopos}})
                    result[order.customer.user.username]['order'].append(i[-6:])
                else:
                    result[order.customer.user.username]['order'].append(i[-6:])
            else:
                print('ERROR')
    text = ""
    for u in result:
        text += f"Customer: name: {result.get(u).get('name')}, email: {result.get(u).get('email')}, ip: {result.get(u).get('ip')}, country: {result.get(u).get('country')} \
        \norders: {result.get(u).get('order')} \
        \n---------------------------------------------------------------------------------\n"
    print(text)
    
# fraud_check()
