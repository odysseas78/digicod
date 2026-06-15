# import os
# import time
# from eshop.models import *
# import django
# import requests
# from django.conf import settings

# def random_code(length=16, low=True, up=True, num=True, spchr=True):
#     import secrets
#     lower = "abcdefghijklnopqrstuvwxyz"
#     uper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
#     number = "1234567890"
#     spchar = "+-/*!&$#?=@<>"
#     chars = ""
#     if low == True:
#         chars += lower
#     if up == True:
#         chars += uper
#     if num == True:
#         chars += number
#     if spchr == True:
#         chars += spchar
#     return ''.join([secrets.choice(chars) for i in range(length)])

# def prod_order_controller(order):
#     products = order.cart.products.all()
#     for cp in products:
#         if cp.product.brand.wsaler == 'Prepaidforge':
