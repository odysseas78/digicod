from datetime import date, datetime, timedelta
from time import sleep
import os, sys



dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(2, parent_dir_path)
# os.environ['PYTHONPATH'] = '/home/user/.cache/pypoetry/virtualenvs/dcback-po_-vPs_-py3.10/bin/python:'+os.path.dirname(os.path.realpath(__file__))
# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
# import django
# django.setup()
import json
from django.core.mail import send_mail
from eshop.PrepaidForge.PF import get_all_products, set_prices
from eshop.currency_prices import get_cur_prices
from eshop_api.utils import cancell_orders, Verify
from eshop.crypto.bnce import set_crypto_prices, crypto_pay_check
from eshop.Utilss.utils import worders_reprocess
from eshop.models import BlackList
from eshop.kinguin.products import getprod
from eshop.payment.utils_payment import BlList


def main():
    reset = datetime.now() - timedelta(days=10)
    reset2 = datetime.now() - timedelta(days=10)
    reset3 = datetime.now() - timedelta(days=10)
    reset4 = datetime.now() - timedelta(days=10)
    reset5 = datetime.now() - timedelta(days=10)
    
    while True:
        sleep(1)
        if reset < (datetime.now() - timedelta(hours=1)):
            try:
                get_all_products()
                set_prices()
                cancell_orders()
            except Exception as d:
                send_mail('Products Prices sinc', str(d), 'info@digicod.eu', ['admin@digicod.eu'], fail_silently=False)
            reset = datetime.now()

        if reset2 < (datetime.now() - timedelta(hours=3)):
            try:
                get_cur_prices()
            except Exception as d:
                send_mail('Currency prices', str(d), 'info@digicod.eu', ['admin@digicod.eu'], fail_silently=False)
            try:
                worders_reprocess()
            except Exception as d:
                send_mail('Currency prices', str(d), 'info@digicod.eu', ['admin@digicod.eu'], fail_silently=False)
            reset2 = datetime.now()

        if reset3 < (datetime.now() - timedelta(minutes=3)):
            try:
                getprod(prodid=None)
            except Exception as d:
                pass
            try:
                set_crypto_prices()
                #-------pending worders check----------------------------
                # worders = WalletOrder.objects.filter(status='pending_payment')
                # for worder in worders:
                #     check_process_order(request=None, order=None, worder=worder)
                #-----------------------------------------------------------
                Verify.calbck_recheck()
                #-----------------------------------------------------------
            except Exception as d:
                send_mail('set_crypto_prices', str(d), 'info@digicod.eu', ['admin@digicod.eu'],
                          fail_silently=False)
            reset3 = datetime.now()

        if reset4 < (datetime.now() - timedelta(seconds=30)):
            try:
                crypto_pay_check()
            except Exception as d:
                send_mail('crypto_payment_checker', str(d), 'info@digicod.eu', ['admin@digicod.eu'], fail_silently=False)
            try:
                qs = BlackList.objects.all()
                if qs:
                    s = set(qs.values_list('description'))
                    for vl in s:
                        v = json.loads(vl[0])
                        BlList(checktime=v.get('checktime'), count=v.get('count'), bltime=v.get('bltime'), appid=v.get('appid')).bl_clear()
            except:
                pass
            reset4 = datetime.now()


if __name__ == "__main__":
    main()
