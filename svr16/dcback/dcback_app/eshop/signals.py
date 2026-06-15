import asyncio, os, sys, json, django
import time
# sys.path.insert(0, '/home/dcback')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
from django.db.models.signals import post_save,pre_save, class_prepared
from django.dispatch import receiver
from eshop.models import Orders, Brand, Product
from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer
from loguru import logger
from django.apps import AppConfig
from django.core.signals import request_started
from lib.PersistentDictObj import PersistentDictObj

ob = PersistentDictObj(file_path='/home/dcback/eshop/signals', jsononly=True)

# @receiver(pre_save, sender=Brand)
# def my_callback(sender, **kwargs):
#     ob.signal1 = 'Brand'
#     ob.zeit = time.time()
# @receiver(post_save, sender=Product)
# def my_callback(sender, **kwargs):
#     ob.signal1 = sender
#     ob.zeit = time.time()
# def logfn1(name,path='logs/'):
#     logger.add(f"{path}/{name}.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == name)
#     return logger.bind(name=name)


# @receiver(post_save, sender=Orders)
# def notify_order_status(sender, instance, **kwargs):
#     print('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWw')
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         f"user_{instance.basket.owner.user.id}",  # Benutzergruppe
#         {
#             "type": "send_update",
#             "message": {
#                 "order_id": instance.id,
#                 "product_name": instance.id,
#                 "status": instance.status,
#             },
#         }
#     )
    
    
@receiver(post_save, sender=Orders)
def publish_event(instance, **kwargs):
    event = {
        # "model": instance.content_type.name,
        # "object": instance.object_repr,
        # "message": instance.get_change_message(),
        # "timestamp": instance.action_time.isoformat(),
        "user": str(instance.basket.owner.user.id),
        # "content_type_id": instance.content_type_id,
        "object_id": instance.id,
    }
    # connection = get_redis_connection("default")
    
    payload = json.dumps(event)
    # logfn1('signal','eshop').info(payload)
    # connection.publish("event", payload)



