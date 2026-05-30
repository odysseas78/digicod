from django.db import models
from ctypes import addressof
import decimal
import json
from eshop.wallet.wallet import CoinWallet, CoinWalletTransaction, CoinWalletSegment
from loguru import logger
# from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from eshop.models_kinguin import *
from eshop.models_utils import *
from datetime import datetime, timedelta, timezone
from lib.PersistentDictObj import DictObj, PersistentDictObj
import pickle
import uuid
from django.conf import settings
from apps.textchoices import *

User = get_user_model()

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra_data = models.JSONField(default=dict, blank=True)

    class Meta:
        abstract = True

class UserPasskey(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="passkeys",
    )

    name = models.CharField(max_length=120, blank=True, default="")
    credential_id = models.BinaryField(unique=True)
    public_key = models.BinaryField()
    sign_count = models.BigIntegerField(default=0)

    device_type = models.CharField(max_length=50, blank=True, default="")
    backed_up = models.BooleanField(default=False)
    transports = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.name or 'Passkey'}"  


class Customer(User):

    user = models.OneToOneField(User, verbose_name='User', related_name='customer_user', on_delete=models.CASCADE, primary_key=True)
    phone = models.CharField(max_length=20, verbose_name='Phone', null=True, blank=True)
    street = models.TextField(verbose_name='Street', null=True, blank=True)
    street2 = models.CharField(max_length=255, verbose_name='Street', null=True, blank=True)
    city = models.CharField(max_length=255, verbose_name='City', null=True, blank=True)
    subdivision = models.CharField(max_length=255, verbose_name='subdivision', null=True, blank=True)
    postal_code = models.CharField(max_length=255, verbose_name='Postal code', null=True, blank=True)
    date_of_birth = models.DateField(verbose_name='date_of_birth', null=True, blank=True)
    country_code = models.CharField(max_length=20, verbose_name='Country', null=True, blank=True)
    rolle = models.CharField(max_length=20, verbose_name='Rolle', null=True, blank=True)
    status = models.CharField(max_length=20, verbose_name='Status', null=True, blank=True)
    add_info = models.JSONField(verbose_name='json', null=True, blank=True, default=dict)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        ordering = ['-user__id']

    def __str__(self):
        if not (self.user.first_name and self.user.last_name):
            return "{} - {}".format(self.user.id, self.user.username)
        return "{} - {} - {} {}".format(self.user.id, self.user.username, self.user.first_name, self.user.last_name)