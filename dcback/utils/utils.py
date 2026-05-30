import json
import pickle
from unicodedata import decimal
from unittest import result
from eshop.payop.functions import check_inv_status
from django.core.mail import send_mail
import ast
from loguru import logger
import os.path
from datetime import datetime, timedelta
import decimal
from decimal import Decimal
import requests
from config import settings


def dictKeys(data, level=0):
    result = []
    def get_keys_from_nested_dict(data, level):
        if isinstance(data, dict):
            for key in data:
                result.append(f'Level {level} : {key}')
                # ddd(result)
                get_keys_from_nested_dict(data[key], level + 1)
        elif isinstance(data, list):
            for item in data:
                get_keys_from_nested_dict(item, level)
        
    get_keys_from_nested_dict(data, level)
    return result

def random_code(length=16, low=True, up=True, num=True, spchr=True):
    import secrets
    lower = "abcdefghijklnopqrstuvwxyz"
    uper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    number = "1234567890"
    spchar = "+-/*!&$#?=@<>"
    chars = ""
    if low == True:
        chars += lower
    if up == True:
        chars += uper
    if num == True:
        chars += number
    if spchr == True:
        chars += spchar
    return ''.join([secrets.choice(chars) for i in range(length)])

class DictObj:
    def __init__(self, in_dict:dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
               setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
               setattr(self, key, DictObj(val) if isinstance(val, dict) else val)
               
    def to_dict(self):
        out_dict = {}
        for key, val in self.__dict__.items():
            if isinstance(val, DictObj):
                out_dict[key] = val.to_dict()
            elif isinstance(val, (list, tuple)):
                out_dict[key] = [item.to_dict() if isinstance(item, DictObj) else item for item in val]
            else:
                out_dict[key] = val
        return out_dict


def listUniq(obj):
    s = set()
    l = list()
    for a in obj:
        s.add(json.dumps(a))
    for b in list(s):
        l.append(json.loads(b))
    return l



def save_obj(obj, filename):
    with open(filename+'.obj', 'wb') as dictionary_file:
        # Step 3
        pickle.dump(obj, dictionary_file)


def read_obj(file):
    with open(file+'.obj', 'rb') as dictionary_file:
        # Step 3
        return pickle.load(dictionary_file)

def get_data():
    from eshop.models import Jsonfile
    a = Jsonfile.objects.filter(name='Shopsettings').first().json
    b = 10
    return b

def json_read(file):
    if not os.path.exists(file):
        out_file = open(file, "w")
        json.dump({}, out_file, indent=2)
        out_file.close()
    with open(file, 'r') as file:
        try:
            return json.load(file)
        except Exception as d:
            return {}


def json_save(data, file):
    out_file = open(file, "w")
    json.dump(data, out_file, indent=2)
    out_file.close()


def get_or_create_token(username):
    from rest_framework.authtoken.models import Token
    from eshop.models import User
    token = Token.objects.filter(user__username=username).first()
    if token:
        return token.key
    else:
        user = User.objects.filter(username=username).first()
        create = Token.objects.create(user=user)
        return create.key


def create_token(request):
    from rest_framework.authtoken.models import Token
    # from eshop.models import User
    token = Token.objects.filter(user=request.user).first()
    if token:
        token.delete()
        create = Token.objects.create(user=request.user)
        return create.key
    else:
        return None

# @logger.catch(message='check_process_order')
# def check_process_order(request, order, worder):
#     from eshop.models import PaymentCallback, Jsonfile, Wallet
#     from eshop_api.utils import callbck_check, wallet_transaction
#     from eshop.soap_neosurf import soap_get_trx_detail
#     from eshop.PrepaidForge.Order import pf_product_order
#     from eshop.order_email_send import orderemail
#     from eshop.kinguin.order import kinguin_product_order
#     from eshop.crypto.merchant import query_order

    
#     settings=Jsonfile.objects.filter(name='Shopsettings').first().json
#     if not settings.get('Other').get('TestModus'):
#         test = 'no'
#     else:
#         test = 'yes'
#     if order:
#         aprove = False
#         if order.status == "pending_payment":
#             order.status = 'processing'
#             order.save()
#             if order.invoice:
#                 inv = ast.literal_eval(order.invoice)
#                 identif = inv.get('data').get('identifier')
#                 result = check_inv_status(identif)
#                 if result.json().get('data').get('status') == 'success':
#                     aprove = True
#                     order.status = 'processing'
#                     order.save()

#             elif not order.invoice:
#                 if order.cart.payment_method.name == "Neosurf":
#                     pc = PaymentCallback.objects.filter(order=order).first()
#                     if request and request.POST.get('hash') and not pc:
#                         PaymentCallback.objects.create(order=order, data=request.POST)
#                         hash = callbck_check(request)
#                         if request.POST.get("status") == "ok" and hash == request.POST.get('hash'):
#                             aprove = True
#                             order.status = 'processing'
#                             order.save()
#                     else:
#                         if pc:
#                             if not pc.check_order:
#                                 trx = soap_get_trx_detail(order.id, test)
#                                 pc.check_order = trx
#                                 pc.save()
#                         elif not pc:
#                             trx = soap_get_trx_detail(order.id, test)
#                             PaymentCallback.objects.create(order=order, check_order=trx)
#                             if trx.get('status') == 'ok':
#                                 aprove = True
#                                 order.status = 'processing'
#                                 order.save()
#                 elif order.cart.payment_method.name == "Binance Pay":
#                     res = query_order(merchantTradeNo=order.id)
#                     if res and res.get('data').get('status') == 'PAID':
#                         aprove = True
#                         order.status = 'processing'
#                         order.save()

#                 elif order.cart.payment_method.name == "Cryptocurrency":
#                     if order.postdata == 'paid':
#                         aprove = True
#                         order.status = 'processing'
#                         order.save()
                
            
#         if aprove:
#             if order.cart.wallet_payment > 0:
#                 # wallet = Wallet.objects.filter(owner=order.customer).first()
#                 wallet_transaction(order.customer, 'debit', -order.cart.wallet_payment,
#                                    f'Payment for order #{order.id}')
            
#             pf_roducts = order.cart.products.filter(product__brand__wsaler='Prepaidforge')
#             kinguin_products = order.cart.products.filter(product__brand__wsaler='Kinguin')
#             list_res = []
#             if pf_roducts:
#                     pfres = pf_product_order(order, pf_roducts)
#                     list_res.append(pfres)
#             if kinguin_products:
#                     kinres = kinguin_product_order(order, kinguin_products)
#                     list_res.append(kinres)
#             for r in list_res:
#                 if r == 'ok':
#                     final_res = 'ok'
#                 else:
#                     final_res = 'error'
#                     break
#             if final_res == 'ok':
#                 rch = RabattCeck(order)
#                 rch.walletcredit()
#                 order.status = 'completed'
#                 order.save()
#             orderemail(order.id)
#             order.save()
#             order.cart.save()
#             return True
#         else:
#             order.status = 'pending_payment'
#             order.save()
#             return False

#     if worder:
#         aprove = False
#         if worder.status == 'pending_payment':
#             worder.status = 'processing'
#             worder.save()
#             if worder.invoice:
#                 inv = ast.literal_eval(worder.invoice)
#                 identif = inv.get('data').get('identifier')
#                 result = check_inv_status(identif)
#                 if result.json().get('data').get('status') == 'success':
#                     aprove = True
#                     worder.status = 'processing'
#                     worder.save()
#             else:
#                 if worder.payment_method.name == 'Neosurf':
#                     pc = PaymentCallback.objects.filter(worder=worder).first()
#                     if request and request.POST.get('hash') and not pc:
#                         PaymentCallback.objects.create(worder=worder, data=request.POST)
#                         hash = callbck_check(request)
#                         if request.POST.get("status") == "ok" and hash == request.POST.get('hash'):
#                             aprove = True
#                             worder.status = 'processing'
#                             worder.save()
#                     else:
#                         trx = soap_get_trx_detail(worder.id, test)
#                         if not pc:
#                             PaymentCallback.objects.create(worder=worder, check_order=trx)
#                         elif not pc.check_order:
#                             pc.check_order = trx
#                             pc.save()
#                         if trx.get('status') == 'ok':
#                             aprove = True
#                             worder.status = 'processing'
#                 elif worder.payment_method.name == 'Binance Pay':
#                     res = query_order(merchantTradeNo=worder.id)
#                     if res and res.get('data').get('status') == 'PAID':
#                         aprove = True
#                         worder.status = 'processing'
#                         worder.save()

#                 elif worder.payment_method.name == 'Cryptocurrency':
#                     if worder.postdata == 'paid':
#                         aprove = True
#                         worder.status = 'processing'
#                         worder.save()
                
#         if aprove:
#             descript = f'Top-Up with {worder.payment_method.name} #{worder.id}'
#             wallet = Wallet.objects.filter(description=descript).first()
#             if wallet:
#                 return False
#             tr = wallet_transaction(worder.owner, 'credit', worder.price / worder.currency.price,
#                                     descript)
#             if tr:
#                 worder.status = 'completed'
#                 worder.save()
#                 return True
#             else:
#                 return False
#         else:
#             worder.status = 'pending_payment'
#             worder.save()
#             return False
#     return False
            
            
def parsedict(data, typ):
    # datac = data.copy()
    max = {}
    result = {}
    def strtofloat(objc):
        for key, val in objc.items():
            if val and (type(val) is str or type(val) is int):
                try:
                    type(float(val[0]))
                except:
                    pass
                try:
                    val = float(val)
                except:
                    val = val.replace(',', '.')
                    val = float(val)
                    objc.update({key:val})
                objc.update({key:val})
            if type(val) is dict:
                strtofloat(val)
        return objc
    def parse(data2):
        data2c = data2.copy()
        for key, value in data2c.items():
            if key == 'currencyes':
                result.update({key:value})
            if type(value) is not dict:
                if not max.get(key):
                    max.update({key:[value]})
                else:
                    max[key].append(value)
            if type(value) is dict:
                parse(value)
    datac = strtofloat(data)
    for k, v in typ.items():
        if v in datac.get('name').keys():
            parse(datac.get('name').get(v))
            break
    
    for k, v in max.items():
        if not result.get('max'):
            result.update({'max':{k:sorted(v,reverse=True)[0]}})
        else:
            result.get('max').update({k:sorted(v,reverse=True)[0]})
    
    
    return result


def limitcheck(request):
    from eshop.models import Orders, Limit, Basket
    from django.db.models import Q
    
    basket = Basket.objects.get(owner=request.user.customer, in_order=False)    
    def getorders():
        res = {}
        try:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        except:
            try:
                ip = request.META['REMOTE_ADDR']
            except:
                ip = request.META.HTTP_X_FORWARDED_FOR
        i=0
        while i < 2:
            q_object = Q()
            if i == 1:
                q_object = Q(basket__currency=basket.currency)
            orders = Orders.objects.filter(q_object).filter(Q(basket__owner=request.user.customer))\
                .exclude(Q(status='cancelled') | Q(status='refunded') | Q(status='pending_payment'))
            now = datetime.now()
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            dayqs = orders.filter(created_at__gte=start_of_day)
            weekqs = orders.filter(created_at__gt=datetime.today() - timedelta(days=datetime.today().isocalendar()[2] + 1))
            monthqs = orders.filter(created_at__gt=datetime.today() - timedelta(days=datetime.today().day))
            day = sum([dayqs.basket.total_price for dayqs in dayqs]) + basket.total_price
            week = sum([weekqs.basket.total_price for weekqs in weekqs])  + basket.total_price
            month = sum([monthqs.basket.total_price for monthqs in monthqs])  + basket.total_price
            if i == 0:
                res.update({'all': {'day':day, 'week': week, 'month': month}})
            else:
                res.update({basket.currency.shortname: {'day':day, 'week': week, 'month': month}})
            i+=1
        return res
        
    
    def check(data):
        # priority CUSTOMER => ROLLE => GLOBAL
        def getlimit():
            limitqs = Limit.objects.filter(active=True, deleted=False, category='order')
            limit = limitqs.filter(customer=request.user.customer).first()
            if limit:
                return limit
            limit = limitqs.filter(name=request.user.customer.rolle).first()
            if limit:
                return limit
            limit = limitqs.filter(name='global').first()
            if limit:
                return limit
            return False
            
        getres = getlimit()
        result = False
        if getres:
            if data.get('all').get('day') > getres.daily:
                result = 'daily'
            if data.get('all').get('week') > getres.weekly:
                result = 'weekly'
            if data.get('all').get('month') > getres.monthly:
                result = 'monthly'
        return result
                                           
                   
    return check(getorders())


def wolimitcheck(request, curr):
    from eshop.models import Cart, Order, Limit, WalletOrder
    from django.db.models import Q
    curamount = decimal.Decimal(request.data['total_price']) / curr.price
    # print(f"{decimal.Decimal(price.get('data')['total_price'])} * {curr.price} | {decimal.Decimal(price.get('data')['total_price']) * curr.price}")
    def getworders():
        try:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        except:
            ip = request.META['REMOTE_ADDR']
        worders = WalletOrder.objects.filter(created_at__gte=datetime.today() - timedelta(days=35)).filter(Q(owner=request.user.customer) | Q(ip=ip))\
            .filter(Q(status='completed') | Q(status='pending_payment'))
        now = datetime.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        dayqs = worders.filter(created_at__gte=start_of_day)
        weekqs = worders.filter(created_at__gte=datetime.today() - timedelta(days=datetime.today().isocalendar()[2] + 1))
        monthqs = worders.filter(created_at__gte=datetime.today() - timedelta(days=datetime.today().day))
        day = sum([dayqs.europrice for dayqs in dayqs]) + curamount
        week = sum([weekqs.europrice for weekqs in weekqs]) + curamount
        month = sum([monthqs.europrice for monthqs in monthqs]) + curamount
        return {'daily':day, 'weekly':week, 'monthly':month}
        
    
    def check(data):
        # priority CUSTOMER => ROLLE => GLOBAL
        def getlimit():
            limitqs = Limit.objects.filter(active=True, deleted=False, category='worder')
            limit = limitqs.filter(customer=request.user.customer).first()
            if limit:
                return limit
            limit = limitqs.filter(name=request.user.customer.rolle).first()
            if limit:
                return limit
            limit = limitqs.filter(name='global').first()
            if limit:
                return limit
            return False
            
        getres = getlimit()
        result = False
        if getres:
            if data.get('daily') > getres.daily:
                result = 'daily'
            if data.get('weekly') > getres.weekly:
                result = 'weekly'
            if data.get('monthly') > getres.monthly:
                result = 'monthly'
        return result
                                           
                   
    return check(getworders())


def worders_reprocess():
    from django.db.models import Q
    from eshop.models import WalletOrder
    from pytz import utc
    from eshop.Utilss.utils import check_process_order, read_obj, save_obj
    from datetime import datetime, timedelta, timezone
    qs = WalletOrder.objects.filter(Q(created_at__lt=datetime.now(utc) - timedelta(hours=2)))
    proc = qs.filter(Q(status='processing'))
    if proc:
        proc.update(status='pending_payment')
    worders = qs.filter(Q(status='pending_payment'))
    sum = 0
    count = 0
    if worders:
        sum = 0
        count = 0
        for item in worders:
            res = check_process_order(None, None, item)
            if res == True:
                sum += item.europrice
                count += 1
            else:
                item.status = 'cancelled'
                item.save()
    try:
        obj = read_obj('woreprocess')
    except Exception as exc:
        save_obj([],'woreprocess')
        obj = read_obj('woreprocess')
    obj.append([datetime.now().timestamp(),count,sum])
    save_obj(obj,'woreprocess')
    
    
    
    

def ConvertQuerysetToJson(qs):
    if qs == None:
        return "Please provide valid Django QuerySet"
    else:
        json_data = []
        for i in qs:
            i = i.__dict__
            i.pop("_state")
            json_data.append(i)
    return json_data