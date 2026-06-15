import os
import sys

import requests

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()
from eshop.models import Currency


def get_cur_prices():
    resp = requests.get('http://api.exchangeratesapi.io/v1/latest?access_key=02cfdf285d2782a517bf32ac4a748210').json()
    qs = Currency.objects.all()
    for item in qs:
        for cur in resp['rates']:
            if cur == item.shortname:
                item.orig_price = resp['rates'][cur]
                item.save()

