import os, sys, django, requests
sys.path.insert(0, '/home/dcback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from pprint import pprint
import json, jsons
from eshop.Utilss.utils import save_obj, read_obj, listUniq

# from rest_framework.authtoken.models import Token

# tokens = Token.objects.all()
# tokens.delete()

from eshop.models import Polzov, User, Cart
# carts = Cart.objects.filter(for_anonymous_user=True, in_order=False)
# carts.delete()
# print(carts)
# res = requests.post('https://odys.digicod.eu/api/gate/',{'malakies':123456789})

# print(res.text)
