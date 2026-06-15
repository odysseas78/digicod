#!/usr/bin/env python
import django
import asyncio, os, sys
sys.path.insert(0, '/home/dcback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
import asyncio
from time import sleep

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_notification_to_group(message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications",
        {
            "type": "send_notification",
            "message": message,
        }
    )

send_notification_to_group('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')