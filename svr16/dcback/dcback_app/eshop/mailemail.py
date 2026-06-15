import asyncio, os, sys, json, django
sys.path.insert(0, '/home/dcback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
from django.core.mail import send_mail
from loguru import logger


@logger.catch
def msend(uid, token):

    send_mail(
        'Test email einstellungrn',
        f'{uid} is{token} the message.',
        'order@digicod.eu',
        ['coxah@web.de','o.martasidis@yahoo.de', 'm.odysseas78@gmail.com'],
        fail_silently=True,
    )

# msend('wqe4tqwe', 'asdy5yadas')

