import django, os, redis
os.system('PYTHONPATH=/home/user/.cache/pypoetry/virtualenvs/dcback-po_-vPs_-py3.10:$PWD')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from eshop.models import Order
from eshop.order_email_send import orderemail
from eshop.Utilss.utils import check_process_order

# order = Order.objects.get(id=871732)
# check_process_order(None, order, None)
# orderemail(871730)

