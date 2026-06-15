import os
# import django

# os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
# django.setup()
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# from shop import settings
from loguru import logger
import json
import re
from collections import OrderedDict
from datetime import datetime, timezone, timedelta
import hashlib
import jsons
import time
import requests
# import socket
# import socks
# ip='127.0.0.10' # change your proxy's ip
# port = 6000 # change your proxy's port
# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
# socket.socket = socks.socksocket





from django.core.mail import send_mail

from .functions import *

# logger.add("safetypay_error.log", backtrace=False, diagnose=True, format="{time} {level} {message}")

# @logger.catch(message='safetypay_send')

def banktr_pay_send(type, orderqs, id, amount, currency, urlOk, urlKo, email, name, date_of_birth, ip, payoption):
    
    if type == 'o':
        items = []
        for cp in orderqs.cart.products.all():
            item = {'id':'','name':'','price':''}
            item['id']=str(cp.product.id)
            item['name']=str(cp.product.title)
            item['price']=str(cp.final_price)
            items.append(item)
    else:
        items = [{'id':str(id),'name':'Wallet top-up', 'price': str(amount)}]

    result = create_invoice(paymentMethod=payoption, amount=str(amount), currency=currency, items=items, orderid=str(id), 
                            useremail=email, fullname=name, resultUrl=urlOk, failPath=urlKo).json()
    if result.get('status') != 1:
        return {"detail": "fault", "message": 'There has been an error. Try again later or contact support.'}
    identifier = result.get('data')

    result = get_invoice(identifier).json()
    orderqs.invoice = result
    orderqs.save()
    logger.info(f'identifier 1 {identifier}')
    if result.get('status') != 1:
        return {"detail": "fault", "message": 'There has been an error. Try again later or contact support.'}
    i = 0
    while i < 6:
        i += 1
        try:
            logger.info(f'identifier 2 {identifier}')
            resp = create_checkout(invid=identifier, customer={'email': email, 'name': name, 
                                    'date_of_birth': date_of_birth.strftime("%d.%m.%Y"), 'ip': ip}, paymentMethod=None, 
                                   payCurrency=currency, card=None, orderid=str(id))
            logger.info(f'order {id}')
            logger.info(f'status_code {resp.status_code}')
            logger.info(f'resp: {resp.content}')
            if resp.status_code != 504:
                result = resp.json()
                logger.info(f'result: {result}')
                if result.get('data'):
                    if result.get('data').get('isSuccess') == True and result.get('status') == 1:
                        txid = result.get('data').get('txid')
                        break
            logger.info(f'identifier 3 {identifier}')
            result = check_inv_status(identifier).json()
            logger.info(f'check_inv_status 1 {result}')
            if result.get('data'):
                if result.get('data').get('isSuccess') == True and result.get('status') == 1:
                    break
            else:
                time.sleep(2)
        except:
            logger.exception("create_checkout")
        time.sleep(2)

    logger.info(f'identifier 4 {identifier}')
    result = check_inv_status(identifier).json()
    logger.info(f'check_inv_status 2 {result}')
    if result.get('data'):
        if result.get('data').get('isSuccess') != True or result.get('status') != 1 or result.get('data').get('status') != 'pending':
            return {"detail": "fault", "message": 'There has been an error. Try again later or contact support.'}
    else:
        return {"detail": "fault", "message": 'There has been an error. Try again later or contact support.'}

    return {"detail": "OK", "url": result.get('data').get('form').get('url')}

