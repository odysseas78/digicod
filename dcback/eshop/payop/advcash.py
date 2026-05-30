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
import requests
import hashlib
import jsons
import time
from django.http import HttpResponse, HttpResponseRedirect
from requests.structures import CaseInsensitiveDict

# import socket
# import socks
# ip='127.0.0.10' # change your proxy's ip
# port = 6000 # change your proxy's port
# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
# socket.socket = socks.socksddddddocket





from django.core.mail import send_mail

from .functions import *

@logger.catch(message='neosurf_payop_send')
def advcash_payop_send(type, orderqs, id, amount, currency, urlOk, urlKo, email, name, ip):
    # paymeth = {"EUR":"200008", "GBP":"200028", "AUD":"200009", "CAD":"200007", "CHF":"200010"}
    if type == 'o':
        items = []
        for cp in orderqs.cart.products.all():
            item = {'id':'','name':'','price':''}
            item['id']=str(cp.product.id)
            item['name']=str(cp.product.title)
            item['price']=str(cp.final_price)
            items.append(item)
    else:
        items = [{'id':str(id),'name':'Digipoints top-up', 'price': str(amount)}]

    result = create_invoice(paymentMethod='765',amount=str(amount), currency=currency, items=items, orderid=str(id), 
                            useremail=email, fullname=name, resultUrl=urlOk, failPath=urlKo).json()
    if result.get('status') != 1:
        return {"detail": "fault", "message": 'There has been an error. Try again later or contact support. (1)'}
    identifier = result.get('data')

    result = get_invoice(identifier).json()
    orderqs.invoice = result
    orderqs.save()
    logger.info(f'identifier 1 {identifier}')
    if result.get('status') != 1:
        return {"detail": "fault", "message": 'There has been an error. Try again later or contact support. (2)'}
    i = 0
    while i < 6:
        i += 1
        try:
            logger.info(f'identifier 2 {identifier}')
            resp = create_checkout(invid=identifier, customer={'email': email, 'name': name, 'ip': ip}, paymentMethod=None, 
                                   payCurrency=currency, card=None, orderid=str(id))
            # logger.info(f'order {id}')
            # logger.info(f'status_code {resp.status_code}')
            # logger.info(f'resp: {resp.content}')
            if resp.status_code != 504:
                result = resp.json()
                # logger.info(f'result: {result}')
                if result.get('data'):
                    if result.get('data').get('isSuccess') == True and result.get('status') == 1:
                        txid = result.get('data').get('txid')
                        break
            # logger.info(f'identifier 3 {identifier}')
            result = check_inv_status(identifier).json()
            # logger.info(f'check_inv_status 1 {result}')
            if result.get('data'):
                if result.get('data').get('isSuccess') == True and result.get('status') == 1:
                    break
            else:
                time.sleep(2)
        except:
            logger.exception("create_checkout")
        time.sleep(2)

    # logger.info(f'identifier 4 {identifier}')
    result = check_inv_status(identifier).json()
    # logger.info(f'check_inv_status 2 {result}')
    if result.get('data'):
        if result.get('data').get('isSuccess') != True or result.get('status') != 1 or result.get('data').get('status') != 'pending':
            return {"detail": "fault", "message": 'There has been an error. Try again later or contact support. (3)'}
    else:
        return {"detail": "fault", "message": 'There has been an error. Try again later or contact support. (4)'}

    
    # order = result.get('data').get('form').get('fields')
    return {'detail':'OK','url':f"https://checkout.payop.com/en/payment/invoice-preprocessing/{identifier}"}

    # if test == 'yes':
    #     order.get('test') = 'yes'
    # headers = CaseInsensitiveDict()
    # headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    # headers["Content-Type"] = "application/x-www-form-urlencoded"
    # post_data = order
    # orderqs.postdata = post_data
    # orderqs.save()
    # i=0
    # url = result.get('data').get('form').get('url')
    # resp = requests.post(url, data=post_data, headers=headers)
    
    


