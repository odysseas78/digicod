import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()

from eshop.soap_neosurf import soap_get_trx_detail
from eshop.models import WalletOrder


def main(id, test):
    res = soap_get_trx_detail(id, test)
    print(res)
    
# main(376526, 'no')
# main(449815, 'no')

# wo = WalletOrder.objects.filter(owner__user__id=683).exclude(status='completed')
# print(wo)	
