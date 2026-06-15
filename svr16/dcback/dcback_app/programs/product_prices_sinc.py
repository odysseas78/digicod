from datetime import date, datetime, timedelta

import os, sys



dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(2, parent_dir_path)

# import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
# import django
# django.setup()

from django.core.mail import send_mail
from eshop.PrepaidForge.PF import get_all_products, set_prices
from eshop.currency_prices import get_cur_prices
from programs.backup_pgdatabase import db_bu_upload_gdrive
from eshop_api.utils import cancell_orders, Verify
from eshop.crypto.bnce import set_crypto_prices, crypto_payment_checker
from eshop.Utilss import check_process_order
from loguru import logger
from eshop.models import WalletOrder

logger.add("logs/callbck.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "callbck_log")
callbck_log = logger.bind(name="callbck_log")

def main():
    reset = datetime.now() - timedelta(days=10)
    reset2 = datetime.now() - timedelta(days=10)
    reset3 = datetime.now() - timedelta(days=10)
    reset4 = datetime.now() - timedelta(days=10)
    reset5 = datetime.now() - timedelta(days=10)
    while True:
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
            reset2 = datetime.now()

        if reset3 < (datetime.now() - timedelta(minutes=5)):
            try:
                set_crypto_prices()
                #-------pending worders check----------------------------
                worders = WalletOrder.objects.filter(status='pending_payment')
                for worder in worders:
                    check_process_order(request=None, order=None, worder=worder)
                #-----------------------------------------------------------
                Verify.calbck_recheck()
                #-----------------------------------------------------------
            except Exception as d:
                send_mail('set_crypto_prices', str(d), 'info@digicod.eu', ['admin@digicod.eu'],
                          fail_silently=False)
            reset3 = datetime.now()

        if reset4 < (datetime.now() - timedelta(seconds=20)):
            try:
                crypto_payment_checker()
            except Exception as d:
                send_mail('crypto_payment_checker', str(d), 'info@digicod.eu', ['admin@digicod.eu'], fail_silently=False)
            reset4 = datetime.now()


if __name__ == "__main__":
    main()
