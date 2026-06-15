import decimal
import os
from datetime import datetime, timedelta
from pprint import pprint

import django
import pytz
from django.core.mail import send_mail
from eshop.PrepaidForge.Order import pf_product_order
from eshop.kinguin.order import kinguin_product_order
from eshop.order_email_send import orderemail
from eshop_api.utils import wallet_transaction
import requests
# from config.settings import env_dict

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from binance import Client
import os

from eshop.models import Currency, Order, WalletOrder
from eshop.Utilss.utils import check_process_order

apikey = env_dict.get('bin_digi_key')
secret = env_dict.get('bin_digi_secret')


client = Client(apikey, secret)

# print(apikey)
# print(client.get_deposit_history(coin='USDT', startTime=1646523843798))
# ticker = client.get_all_tickers()

# pairs = 'BTCEUR,USDTEUR,DASHEUR,XMREUR,SOLEUR,ETHEUR,BCHEUR,LTCEUR'
# resp = requests.get('https://api.kraken.com/0/public/Ticker?pair='+pairs)
# print(resp)
def set_crypto_prices():
    prices = client.get_all_tickers()
    base = Currency.objects.filter(base=True).first()
    curqs = Currency.objects.filter(type='crypto')
    for cur in curqs:
        bp = 0
        for item in prices:
            if item['symbol'] == 'BTC' + base.shortname:
                bp = item['price']
        for item in prices:
            if cur.shortname == 'BTC':
                cur.orig_price = round(1 / decimal.Decimal(bp), 8)
                cur.save()
            if item['symbol'] == cur.shortname + 'BTC':
                cur.orig_price = round(1 / decimal.Decimal(item['price']) / decimal.Decimal(bp), 8)
                cur.save()
            if item['symbol'] == 'BTC' + cur.shortname:
                cur.orig_price = round(decimal.Decimal(item['price']) / decimal.Decimal(bp), 8)
                cur.save()

# set_crypto_prices()

def get_adress(asset, network):
    address = client.get_deposit_address(coin=asset, network=network)
    return address


def crypto_pay_check():
    orderqs = Order.objects.filter(status='pending_payment', cart__payment_method__name='Cryptocurrency').order_by('created_at')
    worderqs = WalletOrder.objects.filter(status='pending_payment', payment_method__name='Cryptocurrency').order_by('created_at')
    txidsforcheck = []
    
    for item in orderqs:
        settxids = set(item.json.get('txid'))
        txidsforcheck.extend(list(settxids))

    for item2 in worderqs:
        settxids2 = set(item2.json.get('txid'))
        txidsforcheck.extend(list(settxids2))
        
    dup = {x for x in txidsforcheck if txidsforcheck.count(x) > 1}
    
    if orderqs and worderqs:
        if orderqs.last().created_at >= worderqs.last().created_at:
            date = worderqs.last().created_at
        else:
            date = orderqs.last().created_at
    elif orderqs:
        date = orderqs.last().created_at
        
    elif worderqs:
        date = worderqs.last().created_at
    if orderqs:
        for order in orderqs:
            if order.created_at.timestamp() < (datetime.now() - timedelta(minutes=60)).timestamp():
                order.status = 'cancelled'
                order.save()
                continue
            if len(dup) > 0:
                extlist = []
                ortxids = set(order.json.get('txid'))
                extlist.extend(list(ortxids))
                extlist.extend(list(dup))
                dup2 = {x for x in extlist if extlist.count(x) > 1}
                if len(dup2) > 0:
                    order.status = 'cancelled'
                    order.save()
                    continue
            resp = client.get_deposit_history(startTime=int(1000 * date.timestamp()))
            # resp = client.get_deposit_history(startTime=int(1000 * date.timestamp()))
            # resp = client.get_deposit_history(startTime=int((datetime.now() - timedelta(days=90)).timestamp()*1000))
            # pprint(resp)
            if resp:
                for t in resp:
                    t['txId'] = t.get('txId').replace('Internal transfer ', '')
                sttxids = set(order.json.get('txid'))
                filtered = filter(lambda txid: txid.get('txId') in list(sttxids), resp)
                fltrd = list(filtered)
                if len(fltrd) > 0:
                    summ = decimal.Decimal(0)
                    for itm in fltrd:
                        summ += decimal.Decimal(itm.get('amount'))
                    if summ >= order.pay_amount - (order.pay_amount * decimal.Decimal(0.005)) and itm['coin'] == order.pay_currency.shortname:
                        order.json.update({'recived':str(summ)})
                        order.postdata = 'paid'
                        order.save()
                        check_process_order(None,order,None)
                    else:
                        order.json.update({'recived':str(summ)})
                        order.save()

    if worderqs:
        for worder in worderqs:
            if worder.created_at.timestamp() < (datetime.now() - timedelta(minutes=60)).timestamp():
                worder.status = 'cancelled'
                worder.save()
                continue
            if len(dup) > 0:
                extlist = []
                ortxids = set(worder.json.get('txid'))
                extlist.extend(list(ortxids))
                extlist.extend(list(dup))
                dup2 = {x for x in extlist if extlist.count(x) > 1}
                if len(dup2) > 0:
                    worder.status = 'cancelled'
                    worder.save()
                    continue
            resp = client.get_deposit_history(startTime=int(1000 * date.timestamp()))
            # resp = client.get_deposit_history(startTime=int((datetime.now() - timedelta(days=90)).timestamp()*1000))
            if resp:
                for t in resp:
                    t['txId'] = t.get('txId').replace('Internal transfer ', '')
                sttxids = set(worder.json.get('txid'))
                filtered = filter(lambda txid: txid.get('txId') in list(sttxids), resp)
                fltrd = list(filtered)
                if len(fltrd) > 0:
                    summ = decimal.Decimal(0)
                    for itm in fltrd:
                        summ += decimal.Decimal(itm.get('amount'))
                    if summ >= worder.total_price - (worder.total_price * decimal.Decimal(0.005)) and itm['coin'] == worder.currency.shortname:
                        worder.json.update({'recived':str(summ)})
                        worder.postdata = 'paid'
                        worder.save()
                        check_process_order(None,None,worder)
                    else:
                        worder.json.update({'recived':str(summ)})
                        worder.save()

# crypto_pay_check()

# def main():
#     reset = datetime.now()
#     while True:
#         if datetime.now() - timedelta(seconds=20) > reset:
#             crypto_payment_checker()
#             # print(datetime.now()-reset)
#             reset = datetime.now()
# if __name__ == '__main__':
#     main()
# crypto_payment_checker()
# resp = client.get_deposit_history(startTime=int(1000 * (datetime.now(pytz.UTC) - timedelta(minutes=90)).timestamp()))
# for item in resp:
#     print(item['amount'])
# print(resp[0].get('amount'))
