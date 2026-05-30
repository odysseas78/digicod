from ctypes import addressof
import decimal
import json
import os
import sys
# from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

regions = {
    1:'Europe',
    2:'United States',
    3:'Region free',
    4:'Other',
    5:'Outside Europe',
    6:'RU VPN',
    7:'Russia',
    8:'United Kingdom',
    9:'China',
    10:'RoW (Rest of World)',
    11:'Latin America',
    12:'Asia',
    13:'Germany',
    14:'Australia',
    15:'Brazil',
    16:'India',
    17:'Japan',
    18:'North America'
            }
gernes = [
    'Action',
    'Adventure',
    'Anime',
    'Casual',
    'Co-op',
    'Dating Simulator',
    'Fighting',
    'FPS',
    'Hack and Slash',
    'Hidden Object',
    'Horror',
    'Indie',
    'Life Simulation',
    'MMO',
    'Music / Soundtrack',
    'Online Courses',
    'Open World',
    'Platformer',
    'Point & click',
    'PSN Card',
    'Puzzle',
    'Racing',
    'RPG',
    'Simulation',
    'Software',
    'Sport',
    'Story rich',
    'Strategy',
    'Subscription',
    'Survival',
    'Third-Person Shooter',
    'Visual Novel',
    'VR Games',
    'XBOX LIVE Gold Card',
    'XBOX LIVE Points'
            ]

tags = [
    'indie valley',
    'dlc',
    'base',
    'software',
    'prepaid'
]


class Developers(models.Model):
    product = models.ForeignKey('KinguinProduct', null=True, blank=True, verbose_name='devlp_roduct', related_name='devlp_roduct', on_delete=models.CASCADE)
    developers = models.CharField(max_length=250, verbose_name='developers')
    deleted = models.BooleanField(verbose_name='Deleted', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'


class Publishers(models.Model):
    product = models.ForeignKey('KinguinProduct', null=True, blank=True, verbose_name='publisher_roduct', related_name='publisher_roduct', on_delete=models.CASCADE)
    publishers = models.CharField(max_length=250, verbose_name='publishers')
    deleted = models.BooleanField(verbose_name='Deleted', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'


class Genres(models.Model):
    product = models.ForeignKey('KinguinProduct', null=True, blank=True, verbose_name='gernes_product', related_name='gernes_product', on_delete=models.CASCADE)
    publishers = models.CharField(max_length=250, verbose_name='Gernes')
    deleted = models.BooleanField(verbose_name='Deleted', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'


class Offer(models.Model):
    product = models.ForeignKey('KinguinProduct', null=True, blank=True, verbose_name='offer_product', on_delete=models.CASCADE)
    name = models.CharField(max_length=250, verbose_name='Name', null=True, blank=True)
    offerId = models.CharField(max_length=250, verbose_name='offerId', null=True, blank=True)
    price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='price', null=True, blank=True)
    qty	= models.PositiveIntegerField(default=0, verbose_name='Qty', null=True, blank=True)
    textQty	= models.PositiveIntegerField(default=0, verbose_name='textQty', null=True, blank=True)
    status = models.CharField(max_length=250, verbose_name='Offer Status', null=True, blank=True)
    isPreorder = models.BooleanField(verbose_name="isPreorder", null=True, blank=True)
    releaseDate = models.DateTimeField(auto_now_add=False, verbose_name='releaseDate', null=True, blank=True)
    merchantName = models.CharField(max_length=250, verbose_name='merchantName', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'


class Video(models.Model):
    product = models.ForeignKey('KinguinProduct', null=True, blank=True, verbose_name='video_product', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, verbose_name='title', null=True, blank=True)
    binary = models.BinaryField(verbose_name='binary', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'


class Language(models.Model):
    product = models.ForeignKey('KinguinProduct', null=True, blank=True, verbose_name='language_product', on_delete=models.CASCADE)
    shortname = models.CharField(max_length=250, verbose_name='title', null=True, blank=True)
    longname = models.CharField(max_length=250, verbose_name='title', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'


class SystemRequirement(models.Model):
    product = models.ForeignKey('KinguinProduct', null=True, blank=True, verbose_name='SystemRequirement_Product', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, verbose_name='title', null=True, blank=True)
    description = models.TextField(max_length=2500, verbose_name='description', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'



class Tag(models.Model):
    product = models.ForeignKey('KinguinProduct', null=True, blank=True, verbose_name='tag_Product', on_delete=models.CASCADE)
    tag = models.CharField(max_length=250, verbose_name='tag', null=True, blank=True)
    description = models.TextField(max_length=2500, verbose_name='description', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'


class MerchantName(models.Model):
    product = models.ForeignKey('KinguinProduct', null=True, blank=True, verbose_name='MerchantName_Product', on_delete=models.CASCADE)
    merchantName = models.CharField(max_length=250, verbose_name='tag', null=True, blank=True)
    description = models.TextField(max_length=2500, verbose_name='description', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'



class Image(models.Model):
    product = models.ForeignKey('KinguinProduct', null=True, blank=True, verbose_name='Image_Product', on_delete=models.CASCADE)
    type = models.CharField(max_length=250, verbose_name='tag', null=True, blank=True)
    description = models.TextField(max_length=2500, verbose_name='description', null=True, blank=True)
    path = models.CharField(max_length=250, verbose_name='path', null=True, blank=True)
    url = models.CharField(max_length=250, verbose_name='url', null=True, blank=True)
    binary = models.BinaryField(verbose_name='binary', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'



class Region(models.Model):
    product = models.ForeignKey('KinguinProduct', null=True, blank=True, verbose_name='Region_Product', on_delete=models.CASCADE)
    merchantName = models.CharField(max_length=250, verbose_name='tag', null=True, blank=True)
    description = models.TextField(max_length=2500, verbose_name='description', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'





class KinguinProduct(models.Model):

    product = models.ForeignKey('Product', null=True, blank=True, verbose_name='Product', on_delete=models.CASCADE)
    kinguinId = models.CharField(max_length=250, verbose_name='kinguinId')
    productId = models.CharField(max_length=250, verbose_name='productId')
    cheapestOfferId = models.CharField(max_length=250, verbose_name='cheapestOfferId', null=True, blank=True)
    originalName = models.CharField(max_length=250, verbose_name='originalName', null=True, blank=True)
    description = models.TextField(max_length=2500, verbose_name='description', null=True, blank=True)
    developers = models.ManyToManyField('Developers', related_name='Developers', blank=True)
    publishers = models.ManyToManyField('Publishers', related_name='Publishers', blank=True)
    genres = models.ManyToManyField('Genres', related_name='Genres', blank=True)
    platform = models.CharField(max_length=250, verbose_name='platform', null=True, blank=True)
    releaseDate = models.DateTimeField(auto_now_add=False, verbose_name='releaseDate', null=True, blank=True)
    qty	= models.PositiveIntegerField(default=0, verbose_name='Qty')
    price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='price')
    textQty	= models.PositiveIntegerField(default=0, verbose_name='textQty')
    offers = models.ManyToManyField('Offer', related_name='Genres', blank=True)
    offersCount	= models.PositiveIntegerField(default=0, verbose_name='offersCount')
    totalQty	= models.PositiveIntegerField(default=0, verbose_name='total offers')
    isPreorder = models.BooleanField(verbose_name="isPreorder", null=True, blank=True)
    metacriticScore = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='metacriticScore')
    regionalLimitations = models.CharField(max_length=250, verbose_name='regionalLimitations', null=True, blank=True)
    regionId	= models.PositiveIntegerField(default=0, verbose_name='regionId')
    activationDetails = models.TextField(max_length=2500, verbose_name='activationDetails', null=True, blank=True)
    videos = models.ManyToManyField('Video', related_name='Video', blank=True)
    languages = models.ManyToManyField('Language', related_name='Language', blank=True)
    updatedAt = models.DateTimeField(auto_now_add=False, verbose_name='updatedAt', null=True, blank=True)
    systemRequirements = models.ManyToManyField('SystemRequirement', related_name='SystemRequirement', blank=True)
    tags = models.ManyToManyField('Tag', related_name='tags', blank=True)
    merchantName = models.ManyToManyField('MerchantName', related_name='MerchantName', blank=True)
    ageRating = models.CharField(max_length=250, verbose_name='ageRating', null=True, blank=True)
    steam = models.CharField(max_length=250, verbose_name='Steam app id', null=True, blank=True)
    images = models.ManyToManyField('Image', related_name='Image', blank=True)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        ordering = ['-pk']
        app_label = 'eshop'

    def __str__(self):
        if self.title:
            return "Cartproduct: {}".format(self.title)
        else:
            return "Cartproduct: {}".format(self.product.title)