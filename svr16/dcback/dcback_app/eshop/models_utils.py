from ctypes import addressof
import decimal
import json
import os
import sys
# from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class BlackList(models.Model):
    appid = models.CharField(max_length=255, verbose_name='AppId', null=True, blank=True)
    ip = models.CharField(max_length=255, verbose_name='IP', null=True, blank=True)
    fprint = models.CharField(max_length=255, verbose_name='Fprint', null=True, blank=True)
    id1 = models.CharField(max_length=255, verbose_name='Id1', null=True, blank=True)
    id2 = models.CharField(max_length=255, verbose_name='Id2', null=True, blank=True)
    id3 = models.CharField(max_length=255, verbose_name='Id3', null=True, blank=True)
    id4 = models.CharField(max_length=255, verbose_name='Id4', null=True, blank=True)
    count = models.IntegerField(verbose_name='count', null=True, blank=True, default=0)
    description = models.TextField(blank=True, max_length=255, null=True, verbose_name='Description')
    json = models.JSONField(null=True, blank=True, verbose_name='json')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'
    
    def __str__(self):
        return str([self.fprint, self.ip])
    


class PriceRabatt(models.Model):
    category = models.CharField(max_length=255, verbose_name='category')
    customer = models.ForeignKey('Customer', null=True, blank=True, verbose_name='Customer', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', verbose_name='Brand', on_delete=models.CASCADE, null=True, blank=True)
    brandrabatt = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Brandrabatt %', blank=True,
                                 null=True, default=0)
    product = models.ForeignKey('Product', verbose_name='Product', on_delete=models.CASCADE, null=True, blank=True)
    productrabbat = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Productrabatt %', blank=True,
                                 null=True, default=0)
    description = models.TextField(blank=True, max_length=255, null=True, verbose_name='Description')
    json = models.JSONField(null=True, blank=True, verbose_name='json')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'
    
    def __str__(self):
        return str([self.category, self.brand, self.brandrabatt, self.product, self.productrabbat])
    
    
class UrlToken(models.Model):
    customer = models.ForeignKey('Customer', null=True, blank=True, verbose_name='Customer', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, verbose_name='Description', null=True, blank=True)
    token = models.CharField(max_length=512, verbose_name='Token')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'
    
    def __str__(self):
        return str([self.customer, self.description, self.token, self.created_at, self.updated_at])
        
        
class FingPrint(models.Model):
    fingeprint = models.CharField(max_length=255, verbose_name='Fingerprint', null=True, blank=True, unique=True)
    json = models.JSONField(null=True, blank=True, verbose_name='json')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        ordering = ['-updated_at']
        app_label = 'eshop'
    
    def __str__(self):
        return str([self.created_at, self.updated_at, self.fingeprint])