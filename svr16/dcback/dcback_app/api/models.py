from django.db import models
from django.utils.translation import gettext_lazy as _
from ctypes import addressof
import decimal
import json
# from eshop.wallet.wallet import CoinWallet, CoinWalletTransaction, CoinWalletSegment
# from loguru import logger
# from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
# from eshop.models_kinguin import *
# from eshop.models_utils import *
from datetime import datetime, timedelta, timezone
# from lib.PersistentDictObj import DictObj, PersistentDictObj
import pickle
import uuid
User = get_user_model()

# Create your models here.

class PageItems(models.Model):
	parent = models.CharField(max_length=255, null=True, blank=True)
	items_per_page = models.IntegerField(default=25)
	
class HideShowFilter(models.Model):
	parent = models.CharField(max_length=255, null=True, blank=True)
	key = models.CharField(max_length=255)
	value = models.BooleanField(default=False)

	def __str__(self):
		return self.key

class ModelFilter(models.Model):
	parent = models.CharField(max_length=255, null=True, blank=True)
	key = models.CharField(max_length=255)
	value = models.CharField(max_length=255)

	def __str__(self):
		return self.key
