import sys, os, django, json
from decimal import Decimal
from pprint import pprint
sys.path.insert(0, '/home/dcback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from eshop.Utilss.utils import DictObj
from eshop.wallet.wallet import *
from eshop.models import *
from datetime import datetime, timedelta, timezone
from utils import random_code
from time import sleep





wallet = CoinWallet.objects.filter(user_id=97).first()
# user = get_user_model().objects.get(id=1)
# print(user)
# CoinWallet().create_user_wallet(user=user)
# print(user.coinwallet.balance)
# user.coinwallet.deposit(amount=53.6, purpose='TopUp Neosurf')
# print(user.coinwallet.balance)
# # wallet = CoinWallet()
# # wallet.deposit(100.0)
# wallet.unlock_amount(wallet.locked_balance)
# # print(wallet.add_to_segment(Decimal(-150.78), 'Neosurf top up'))
# print(wallet.balance)  # sollte 50.0 ausgeben
# wallet.refund(Decimal(100.78), 'Refund order #1278349', '', 'gKl8fj6889hkobD8')
# print(wallet.locked_balance)  


# customer = Customer.objects.filter(user_id=97).first()
# user = get_user_model().objects.get(id=97)
# bask = user.customer.basket.filter(in_order=False, owner=None, updated_at__lt=datetime.now()-timedelta(days=2))
# print(bask)

# qs = Product.objects.filter(brand__wsaler='Prepaidforge')

# print(basket.count())
# utcoffset(self, dt)
# print(qs.count())
# ss = user.coinwallet

# print(random_code(16,True,True,True,False))
# class C(object):
#     def __init__(self):
#         self._x = None

#     @property
#     def x(self):
#         """I'm the 'x' property."""
#         print("getter of x called")
#         return self._x

#     @x.setter
#     def x(self, value):
#         print("setter of x called")
#         self._x = value

#     @x.deleter
#     def x(self):
#         print("deleter of x called")
#         del self._x


# c = C()
# c.x = 'foo'  # setter called
# f = c.x 
# print(f)
# k = c.x 
# print(k)
# h = c.x 
# print(h)
# del c.x      # deleter called
# print(f)
# d = c.x 
# print(d)