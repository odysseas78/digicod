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
# from django.contrib.auth.models import AbstractUser
# django.setup()
def logfn1(name,path='logs/'):
    logger.add(f"{path}{name}.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == name)
    return logger.bind(name=name)

User = get_user_model()



class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra_data = models.JSONField(default=dict, blank=True)

    class Meta:
        abstract = True

class Suplier(TimeStampedModel):
    title = models.CharField(max_length=255, verbose_name='Suplier', blank=True, null=True)

class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Category name')
    pf_name = models.CharField(max_length=255, verbose_name='PF category name')
    slug = models.SlugField(unique=True, verbose_name='slug')
    active = models.BooleanField(default=True, verbose_name='active')
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")

    class Meta:
        ordering = ["name"]
        unique_together = ("parent", "name")

    def __str__(self):
        return self.name


    # @property
    # def products(self):
    #     return json.dumps(Product.objects.filter(category=self).values())



class Brand(TimeStampedModel):
    suplier = models.ForeignKey(Suplier, on_delete=models.CASCADE, related_name="brand_suplier", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="brand_category", blank=True, null=True)
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    in_stock = models.BooleanField(verbose_name='In stock', default=True)
    image = models.CharField(null=True, blank=True, max_length=255)
    image2 = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(verbose_name='Description', null=True, blank=True, default=None)
    active = models.BooleanField(verbose_name='Active', default=False)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.title

    # @property
    # def products(self):
    #     return self.products.all()

    def save(self, *args, **kwargs):
        if self.id:
            if self.active == False:
                self.products.all().update(active=False)
            if self.active == True:
                self.products.filter(qty__gt=0).update(active=True)
            
            if self.in_stock == False:
                self.products.all().update(in_stock=False)
            if self.in_stock == True:
                self.products.filter(qty__gt=0).update(in_stock=True)
     
        super().save(*args, **kwargs)
    

class Currency(models.Model):
    type = models.CharField(max_length=255, verbose_name='Type', null=True, blank=True)
    base = models.BooleanField(verbose_name='Base', default=False)
    longname = models.CharField(max_length=255, verbose_name='Longname', null=True, blank=True)
    shortname = models.CharField(max_length=255, verbose_name='Shortname', null=True, blank=True)
    # network = models.ManyToManyField('CryptoNetwork', related_name='related_currency_network', blank=True, verbose_name='Network')
    sign = models.CharField(max_length=255, verbose_name='Sign', null=True, blank=True)
    min_amount = models.DecimalField(max_digits=19, default=0, decimal_places=8, verbose_name='Min amount', null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True, verbose_name='Image')
    image2 = models.CharField(max_length=255, null=True, blank=True, verbose_name='image_svg')
    svg = models.TextField(verbose_name='Svg', null=True, blank=True)
    html = models.TextField(verbose_name='Html', null=True, blank=True)
    price = models.DecimalField(max_digits=19, default=0, decimal_places=8, verbose_name='Price')
    orig_price = models.DecimalField(max_digits=19, default=0, decimal_places=8, verbose_name='Exchange price')
    fee_rate = models.DecimalField(max_digits=19, default=0, decimal_places=8, verbose_name='Fee rate %')
    histori = models.BinaryField(verbose_name='Histori', null=True, blank=True)
    active = models.BooleanField(verbose_name='Active', default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        ordering = ['-type','pk']

    def __str__(self):
        return '{} : {} : {}'.format(self.shortname, self.created_at, self.updated_at)

    def save(self, *args, **kwargs):
        
        shs = PersistentDictObj(file_path='/home/dcback/shop/shopsettings', jsononly=True)
        if not shs.hasattr('currency_exchange_rate'): shs.currency_exchange_rate = 0
        
        glrate = shs.currency_exchange_rate
        if self.shortname != 'EUR':
            if self.fee_rate > 0:
                self.price = decimal.Decimal(self.orig_price) + decimal.Decimal(self.orig_price) * \
                            decimal.Decimal(self.fee_rate) / decimal.Decimal(100)
            else:
                self.price = decimal.Decimal(self.orig_price) + decimal.Decimal(self.orig_price) * \
                            decimal.Decimal(glrate) / decimal.Decimal(100)
        #############################################
        # if self.histori == None:
        #     f = pickle.dumps([])
        #     self.histori=f
        # d = pickle.loads(self.histori)
        # d.append({'date':datetime.now(), 'price':self.price})
        # k = pickle.dumps(d)
        # self.histori=k
        ###############################################
        super().save(*args, **kwargs)


class Product(TimeStampedModel):
    brand = models.ForeignKey(Brand, verbose_name='Brand', related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category", default=None, blank=True, null=True)
    suplier = models.ForeignKey(Suplier, on_delete=models.CASCADE, related_name="product_suplier", blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name='Region', blank=True, null=True)
    image = models.CharField(max_length=255, verbose_name='image', blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price', blank=True,
                                null=True, default=0)
    in_stock = models.BooleanField(verbose_name='In stock', default=True)
    profit_rate = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Profit %', blank=True,
                                 null=True, default=0)
    profit_fixed = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Profit fixed',
                                       null=True,default=0)
    prurchase_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='PF-Price', null=True,
                                   default=False)
    qty = models.PositiveIntegerField(default=0)
    sku = models.CharField(unique=True, max_length=255, verbose_name='Sku', null=True, default=False)
    slug = models.SlugField(unique=True, null=True, default=None, max_length=255)
    gtin = models.CharField(max_length=255, verbose_name='GTIN', blank=True, null=True, default=None)
    ean = models.CharField(max_length=255, verbose_name='EAN', blank=True, null=True, default=None)
    regions = models.CharField(max_length=255, verbose_name='Regions', blank=True, null=True, default=None)
    suplier_product = models.JSONField(verbose_name='suplier_product', default=dict, null=True, blank=True)
    value = models.CharField(max_length=255, verbose_name='Value', null=False, default=None)
    active = models.BooleanField(verbose_name='Active', default=True)
    description = models.TextField(verbose_name='Description', null=True, blank=True, default=None)
    jsondata = models.JSONField(verbose_name='Additional info', default=dict, null=True, blank=True)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return '{} : {} : {} : {} : {}'.format(self.id, self.title, self.brand, self.price, self.region, self.value, self.currency)

    def save(self, *args, **kwargs):
        if self.id:
            self.brand.in_stock = True if self.brand.products.filter(qty__gt=0).count() > 0 else False
            self.brand.save()
            self.in_stock = True if self.qty > 0 else False
            # if not self.image:
            #     self.image = self.brand.image
            ################## Globale profit rate ############################
            dbjsonfile = Jsonfile.objects.filter(name='Shopsettings').first()
            shs = PersistentDictObj(dbjsonfile=dbjsonfile, dbjsonfileonly=True)
            if not shs.hasattr('Prices'): shs.Prices.ProfitRate = 0
            if not shs.hasattr('Prices'): shs.Prices.ProfitRateFix = 0
            prate = shs.Prices.ProfitRate
            pfix = shs.Prices.ProfitRateFix
            ###################################################################
            if self.profit > 0:
                prate = decimal.Decimal(self.profit)
            if self.profit_fixed > 0:
                pfix = decimal.Decimal(self.profit_fixed)
            self.price = decimal.Decimal(self.pf_price) + decimal.Decimal(self.pf_price) * decimal.Decimal(prate) / \
                        decimal.Decimal(100) + decimal.Decimal(pfix)
        super().save(*args, **kwargs)


class ProductCode(models.Model):
    ct_product = models.ForeignKey('CartProduct', verbose_name='CartProduct', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', verbose_name='Order', on_delete=models.CASCADE)
    pf_order_id = models.CharField(max_length=255, verbose_name='PF order Reference')
    orderid = models.CharField(max_length=255, verbose_name='Order ID')
    code = models.CharField(max_length=500, verbose_name='Code')
    serial = models.CharField(max_length=500, verbose_name='Serial')
    downloadLink = models.CharField(max_length=255, verbose_name='Download Link', default='')
    codeType = models.CharField(max_length=100, verbose_name='codeType', default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    def __str__(self):
        return '{} : {}'.format(self.ct_product, self.orderid)
    



class CartProduct(models.Model):

    cart = models.ForeignKey('Cart', verbose_name='Cart', on_delete=models.CASCADE, related_name='cart_products')
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество товара')
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, verbose_name='title')
    product_codes = models.ManyToManyField(ProductCode, blank=True, related_name='related_cart_product')
    currency = models.ForeignKey(Currency, verbose_name='Currency', on_delete=models.CASCADE, default=1)
    order_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Product Order Price')
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Total Price')
    deleted = models.BooleanField(verbose_name='Deleted', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        if self.title:
            return "Cartproduct: {}".format(self.title)
        else:
            return "Cartproduct: {}".format(self.product.title)

    def save(self, *args, **kwargs):
        # if self.qty == 0:
        #     self.delete()
        # if not self.order_price:
        self.currency = self.cart.currency
        if self.cart.in_order == False:
            self.order_price = self.product.price
            self.title = self.product.title
            self.final_price = self.qty * self.order_price
        else:
            self.final_price = int(self.qty) * self.product.price
        super().save(*args, **kwargs)


class ProductCodes(models.Model):
    basket = models.ForeignKey('Basket', verbose_name='Basket', on_delete=models.CASCADE)
    order = models.ForeignKey('Orders', verbose_name='Orders', on_delete=models.CASCADE)
    pf_order_id = models.CharField(max_length=255, verbose_name='PF order Reference')
    orderid = models.CharField(max_length=255, verbose_name='Order ID')
    code = models.CharField(max_length=500, verbose_name='Code')
    serial = models.CharField(max_length=500, verbose_name='Serial', null=True, blank=True)
    downloadLink = models.CharField(max_length=255, verbose_name='Download Link', default='', null=True, blank=True)
    codeType = models.CharField(max_length=100, verbose_name='codeType', default='', null=True, blank=True)
    jsondata = models.JSONField(verbose_name='Additional info', default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    def __str__(self):
        return '{} : {}'.format(self.basket, self.orderid)


class Basket(TimeStampedModel):

    owner = models.ForeignKey('Customer', verbose_name='Customer', related_name='basket', on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey('Orders', verbose_name='Orders', related_name='related_orders', on_delete=models.CASCADE, null=True, blank=True)
    fingprint = models.CharField(max_length=255, verbose_name='FingerPrint', unique=True, null=True, blank=True)
    products = models.ManyToManyField(Product, related_name='basket', verbose_name='Products')
    basket_products = models.JSONField(verbose_name='Basket Products', null=True, blank=True, default=dict)
    total_products = models.PositiveIntegerField(default=0)
    payment_method = models.ForeignKey('Payment', null=True, blank=True, verbose_name='Paymentmethod', related_name='basket', on_delete=models.CASCADE, default=1)
    payment_method_payment = models.DecimalField(max_digits=9, default=decimal.Decimal(0), decimal_places=2, verbose_name='Payment method payment')
    wallet_payment = models.DecimalField(max_digits=9, default=decimal.Decimal(0), decimal_places=2, verbose_name='Wallet payment')
    total_price = models.DecimalField(max_digits=9, default=decimal.Decimal(0), decimal_places=2, verbose_name='Total price')
    final_price = models.DecimalField(max_digits=9, default=decimal.Decimal(0), decimal_places=2, verbose_name='Final price')
    process_fee = models.DecimalField(max_digits=9, default=decimal.Decimal(0), decimal_places=2, verbose_name='Processing fee')
    currency = models.ForeignKey(Currency, verbose_name='Currency', related_name='basket', on_delete=models.CASCADE, default=1)
    addinfo = models.JSONField(verbose_name='Additional info', default=dict, null=True, blank=True)
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def save(self, data=None, *args, **kwargs):
        if self.id:
            if self.in_order:
                self.fingprint = None
            else:
                if not self.basket_products:
                    self.basket_products = dict()
                if data:
                    id = data.get('id')
                    trash = data.get('trash')
                    if trash:
                        self.products.clear()
                        self.basket_products.clear()
                    # wallet = data.get('wallet')
                    currency = data.get('currency')
                    payment = data.get('payment')
                    if data.get('value') != None:
                        qty = int(data.get('value'))
                        if qty > 0:
                            self.products.add(id)
                            product = self.products.filter(id=id).first()
                            # d = self.basket_products
                            self.basket_products.update({str(id):{'title':product.title, 'qty':qty, 'price':float(product.price), 'total':float(product.price) * qty}}) 
                        else:
                            self.products.remove(id)
                            if len(self.basket_products) > 0:
                                self.basket_products.pop(str(id))
                    if currency:
                        self.currency = self.currency._meta.model.objects.get(id=currency)
                    if payment:
                        self.payment_method = self.payment_method._meta.model.objects.get(id=payment) 
                    # if wallet:
                    #     self.wallet_payment = wallet.get('amount')
                
                for p in self.products.all():
                    p.save()
                self.total_products = self.products.count()
                try:
                    self.total_price = sum([product.price * int(self.basket_products.get(str(product.id)).get('qty')) for product in self.products.all()])
                except Exception as d:
                    print(f'basket models  - {d}')
                
                subtotal = self.total_price - self.wallet_payment
                subaddfixfee = subtotal + self.payment_method.fee_fix
                self.process_fee = subaddfixfee * (self.payment_method.fee_rate/100) + self.payment_method.fee_fix if subtotal > 0 else 0
                self.final_price = subtotal + self.process_fee if subtotal > 0 else 0
                self.payment_method_payment = self.final_price - self.wallet_payment
            
        super().save(*args, **kwargs)
   
   
class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Customer', on_delete=models.CASCADE, null=True, blank=True)
    fingprint = models.ForeignKey('FingPrint', verbose_name='fingprint', related_name='fingprint_cart', on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey('Order', verbose_name='order', related_name='related_cart_order', on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    payment_method = models.ForeignKey('Payment', null=True, blank=True, verbose_name='Paymentmethod', on_delete=models.CASCADE, default=1)
    payoption = models.ForeignKey('Payoptions', null=True, blank=True, verbose_name='Payoption', related_name='payopt_cart', on_delete=models.CASCADE)
    payment_method_payment = models.DecimalField(max_digits=9, default=decimal.Decimal(0), decimal_places=2, verbose_name='Payment method payment')
    wallet_payment = models.DecimalField(max_digits=9, default=decimal.Decimal(0), decimal_places=2, verbose_name='Wallet payment')
    final_price = models.DecimalField(max_digits=9, default=decimal.Decimal(0), decimal_places=2, verbose_name='Final price')
    refund_amount = models.DecimalField(max_digits=9, default=decimal.Decimal(0), decimal_places=2, verbose_name='Refund amount')
    process_fee = models.DecimalField(max_digits=9, default=decimal.Decimal(0), decimal_places=2, verbose_name='Processing fee')
    order_final_price = models.DecimalField(max_digits=9, default=decimal.Decimal(0), decimal_places=2, verbose_name='Order final price')
    currency = models.ForeignKey(Currency, verbose_name='Currency', on_delete=models.CASCADE, default=1)
    ex_rate = models.DecimalField(max_digits=19, default=0, decimal_places=8, verbose_name='Ex Rate')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.id:
            [cproduct.save() for cproduct in self.products.all()]
        if self.in_order == False:
            self.ex_rate = self.currency.price
        if not self.owner:
            self.for_anonymous_user = True
            
        if self.id:
            if self.currency.type == 'crypto':
                if self.currency.shortname == 'USDT':
                    tofix = 2
                else:
                    tofix = 8
            else:
                tofix = 2
            self.total_products = self.products.count()
            summ = sum([cproduct.final_price for cproduct in self.products.all()])
            if summ:
                self.final_price = summ
            else:
                self.final_price = decimal.Decimal(0)
            # wallet = Wallet.objects.get(owner=self.owner).balance
            payment = Payment.objects.all()
            
            if self.wallet_payment > decimal.Decimal(0):
                if self.wallet_payment >= self.final_price:
                    self.wallet_payment = self.final_price
                    self.payment_method = payment.get(name='Wallet')
                    
            self.process_fee = self.payment_method.fee_rate / 100 * (self.final_price - self.wallet_payment + self.payment_method.fee_fix) \
                + self.payment_method.fee_fix
            self.payment_method_payment = round((self.final_price - self.wallet_payment) + self.process_fee, tofix)
            self.order_final_price = round(self.final_price + self.process_fee, tofix)

            for p in self.products.all():
                p.save()
            
        super().save(*args, **kwargs)


class Customer(models.Model):

    user = models.OneToOneField(User, verbose_name='User', related_name='customer2_user', on_delete=models.CASCADE, primary_key=True)
    applicant_id = models.CharField(max_length=255, verbose_name='Applicant Id', null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name='Phone', null=True, blank=True)
    street = models.TextField(verbose_name='Street', null=True, blank=True)
    street2 = models.CharField(max_length=255, verbose_name='Street', null=True, blank=True)
    city = models.CharField(max_length=255, verbose_name='City', null=True, blank=True)
    subdivision = models.CharField(max_length=255, verbose_name='subdivision', null=True, blank=True)
    postal_code = models.CharField(max_length=255, verbose_name='Postal code', null=True, blank=True)
    date_of_birth = models.DateField(verbose_name='date_of_birth', null=True, blank=True)
    country_code = models.CharField(max_length=20, verbose_name='Country', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Customer Orders', related_name='related_customer_orders', blank=True)
    ip = models.CharField(max_length=20, verbose_name='IP Address', null=True, blank=True)
    rolle = models.CharField(max_length=20, verbose_name='Rolle', null=True, blank=True)
    status = models.CharField(max_length=20, verbose_name='Status', null=True, blank=True)
    extra = models.TextField(verbose_name='Notes', null=True, blank=True, default=None)
    files = models.ManyToManyField('Verification', verbose_name='Files', related_name='customer_files', blank=True)
    json = models.JSONField(verbose_name='json', null=True, blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    class Meta:
        ordering = ['-user__id']

    def __str__(self):
        if not (self.user.first_name and self.user.last_name):
            return "{} - {}".format(self.user.id, self.user.username)
        return "{} - {} - {} {}".format(self.user.id, self.user.username, self.user.first_name, self.user.last_name)
    

class Orders(models.Model):

    STATUS_PENDING_PAYMENT = 'pending_payment'
    STATUS_IN_PROCESSING = 'processing'
    STATUS_CANCELLED = 'cancelled'
    STATUS_COMPLETED = 'completed'
    STATUS_REFUNDED = 'refunded'

    STATUS_CHOICES = (
        (STATUS_PENDING_PAYMENT, 'Pending payment'),
        (STATUS_IN_PROCESSING, 'Processing'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_REFUNDED, 'Refunded')
    )
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name='uuid', unique=True, db_index=True, editable=False)
    basket = models.ForeignKey(Basket, verbose_name='Basket', related_name='basket',
                                 on_delete=models.CASCADE)
    currency = models.JSONField(verbose_name='Currency', default=dict)
    pay_method = models.JSONField(verbose_name='Payment method', default=dict)
    pay_options = models.JSONField(verbose_name='Payment options', default=dict)
    subtotal = models.JSONField(verbose_name='Total Price', default=dict)
    process_fees = models.JSONField(verbose_name='Process fees', default=dict)
    total = models.JSONField(verbose_name='Final Price', default=dict)
    products = models.JSONField(verbose_name='Products', default=dict)
    del_email = models.CharField(max_length=55, verbose_name='Del Email', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Order Status',
        choices=STATUS_CHOICES,
        default=STATUS_PENDING_PAYMENT
    )
    comment = models.TextField(verbose_name='Comment', null=True, blank=True)
    invoice = models.JSONField(verbose_name='Invoice', default=dict, null=True, blank=True)
    postdata = models.JSONField(verbose_name='Postdata', default=dict, null=True, blank=True)
    responsedata = models.JSONField(verbose_name='Response data', default=dict, null=True, blank=True)
    addinfo = models.JSONField(verbose_name='Additional info', default=dict, null=True, blank=True)
    trash = models.BooleanField(verbose_name='Trash', default=False)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return str(self.id)
    
    def save(self, *args, **kwargs):
        if self.id:
            if self.basket.currency.type == 'crypto':
                if self.basket.currency.shortname == 'USDT':
                    tofix = 2
                else:
                    tofix = 8
            else:
                tofix = 2
            if not self.created_at or self.created_at > datetime.now(timezone.utc) - timedelta(minutes=10):
                self.currency={
                    'code': self.basket.currency.shortname,
                    'price':float(self.basket.currency.price)
                }
                self.subtotal={
                    'a':round(float(self.basket.total_price), tofix),
                    'b':round(float(self.basket.total_price * self.basket.currency.price), tofix)
                }
                self.process_fees={
                    'a':round(float(self.basket.process_fee), tofix),
                    'b':round(float(self.basket.process_fee * self.basket.currency.price), tofix)
                }
                self.total={
                    'a':round(float(self.basket.final_price), tofix),
                    'b':round(float(self.basket.final_price * self.basket.currency.price), tofix)
                }
                self.products=self.basket.basket_products
                self.basket.save()
                self.basket.in_order=True
                self.basket.save()
        super().save(*args, **kwargs)


class CoinWalletDeposit(models.Model):

    STATUS_PENDING_PAYMENT = 'pending_payment'
    STATUS_IN_PROCESSING = 'processing'
    STATUS_CANCELLED = 'cancelled'
    STATUS_COMPLETED = 'completed'
    STATUS_REFUNDED = 'refunded'

    STATUS_CHOICES = (
        (STATUS_PENDING_PAYMENT, 'Pending payment'),
        (STATUS_IN_PROCESSING, 'Processing'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_REFUNDED, 'Refunded')
    )
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name='uuid', unique=True, db_index=True, editable=False)
    coinwallet = models.ForeignKey(CoinWallet, verbose_name='CoinWallet', related_name='coinwallet',
                                 on_delete=models.CASCADE)
    currency = models.JSONField(verbose_name='Currency', default=dict)
    pay_method = models.JSONField(verbose_name='Payment method', default=dict)
    pay_options = models.JSONField(verbose_name='Payment options', default=dict)
    subtotal = models.JSONField(verbose_name='Total Price', default=dict)
    process_fees = models.JSONField(verbose_name='Process fees', default=dict)
    total = models.JSONField(verbose_name='Final Price', default=dict)
    status = models.CharField(
        max_length=100,
        verbose_name='Order Status',
        choices=STATUS_CHOICES,
        default=STATUS_PENDING_PAYMENT
    )
    comment = models.TextField(verbose_name='Comment', null=True, blank=True)
    invoice = models.JSONField(verbose_name='Invoice', default=dict, null=True, blank=True)
    postdata = models.JSONField(verbose_name='Postdata', default=dict, null=True, blank=True)
    responsedata = models.JSONField(verbose_name='Response data', default=dict, null=True, blank=True)
    addinfo = models.JSONField(verbose_name='Additional info', default=dict, null=True, blank=True)
    trash = models.BooleanField(verbose_name='Trash', default=False)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return str(self.id)


class Order(models.Model):

    STATUS_PENDING_PAYMENT = 'pending_payment'
    STATUS_IN_PROCESSING = 'processing'
    STATUS_CANCELLED = 'cancelled'
    STATUS_COMPLETED = 'completed'
    STATUS_REFUNDED = 'refunded'

    STATUS_CHOICES = (
        (STATUS_PENDING_PAYMENT, 'Pending payment'),
        (STATUS_IN_PROCESSING, 'Processing'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_REFUNDED, 'Refunded')
    )
    customer = models.ForeignKey(Customer, verbose_name='Customer', related_name='related_order_customer',
                                 on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, verbose_name='Cart', related_name='order_cart', on_delete=models.CASCADE, null=True, blank=True)
    pay_currency = models.ForeignKey(Currency, verbose_name='pay_currency', on_delete=models.CASCADE, default=1, null=True, blank=True)
    pay_amount = models.DecimalField(max_digits=19, default=0, decimal_places=8, verbose_name='payment amount',
                                     null=True, blank=True)
    europrice = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Euro Price', null=True, blank=True)
    del_email = models.CharField(max_length=55, verbose_name='Del Email', null=True, blank=True)
    ip = models.CharField(max_length=200, verbose_name='IP Address', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Order Status',
        choices=STATUS_CHOICES,
        default=STATUS_PENDING_PAYMENT
    )
    comment = models.TextField(verbose_name='Comment', null=True, blank=True)
    invoice = models.TextField(verbose_name='invoice', null=True, blank=True)
    postdata = models.TextField(verbose_name='Postdata', null=True, blank=True)
    responsedata = models.TextField(verbose_name='Response data', null=True, blank=True)
    json = models.JSONField(verbose_name='json', default=dict)
    trash = models.BooleanField(verbose_name='Trash', default=False)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.id:
            if not self.europrice:
                self.europrice = self.cart.order_final_price
            if self.cart.currency.type == 'crypto':
                if self.cart.currency.shortname == 'USDT':
                    tofix = 2
                else:
                    tofix = 8
            else:
                tofix = 2
            self.pay_currency = self.cart.currency
            if not self.pay_amount:
                self.pay_amount = round(self.cart.order_final_price * self.cart.currency.price, tofix)
            
        super().save(*args, **kwargs)


class Payment(models.Model):
    type = models.CharField(max_length=255, verbose_name='Type', null=True, blank=True)
    provider = models.CharField(max_length=255, verbose_name='Payment Provider', default=None, null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='Payment Name')
    payoptions = models.ManyToManyField('Payoptions', verbose_name='payoptions', related_name='pay_options', blank=True)
    currencies = models.ManyToManyField('Currency', verbose_name='currencies', related_name='related_pay_currencyes', blank=True)
    brands = models.ManyToManyField('Brand', verbose_name='brands', related_name='related_brand_payment', blank=True)
    enabled = models.BooleanField(verbose_name='enabled', default=False)
    desc = models.TextField(verbose_name='Description', null=True, blank=True)
    fee_rate = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Fee %', null=True, blank=True)
    fee_fix = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Fee Fix', null=True, blank=True)
    image = models.CharField(null=True, blank=True, max_length=255)
    image2 = models.CharField(null=True, blank=True, max_length=255)
    svg = models.TextField(verbose_name='Svg', null=True, blank=True)
    html = models.TextField(verbose_name='Html', null=True, blank=True)
    json = models.JSONField(null=True, blank=True, verbose_name='json', default=dict)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    def __str__(self):
        return '{} : {} : {}'.format(self.name, self.fee_rate, self.fee_fix)
    
    
class Payoptions(models.Model):
    payment_method = models.ForeignKey('Payment', null=True, blank=True, verbose_name='Payment', related_name='payopt_paymeth', on_delete=models.CASCADE)
    type = models.CharField(max_length=255, verbose_name='Type', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='Payoption Name')
    # currencies = models.ManyToManyField('Currency', verbose_name='currencies', related_name='related_pay_currencyes', null=True, blank=True)
    # brands = models.ManyToManyField('Brand', verbose_name='brands', related_name='related_brand_payment', null=True, blank=True)
    enabled = models.BooleanField(verbose_name='enabled', default=False)
    desc = models.TextField(verbose_name='Description', null=True, blank=True)
    fee_rate = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Fee %', null=True, blank=True)
    fee_fix = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Fee Fix', null=True, blank=True)
    image = models.CharField(null=True, blank=True, max_length=255)
    image2 = models.CharField(null=True, blank=True, max_length=255)
    svg = models.TextField(verbose_name='Svg', null=True, blank=True)
    html = models.TextField(verbose_name='Html', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    def __str__(self):
        return '{} : {} : {}'.format(self.name, self.payment_method.name, self.enabled)


class ShopSetting(models.Model):
    pf_api_token = models.CharField(max_length=1024, verbose_name='Api token', null=True, blank=True)
    pf_api_token_time = models.PositiveIntegerField(null=True, blank=True)
    pf_test_mode = models.BooleanField(verbose_name='Test mode', default=False)
    profit_rate = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Profit %', null=True, blank=True)
    profit_fixed = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Profit fixed', null=True,
                                        blank=True)
    currency_fee_rate = models.DecimalField(max_digits=9, default=0, decimal_places=4, verbose_name='Currency fee % rate')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    def __str__(self):
        return str(self.pf_api_token_time)


class Limit(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name', blank=True, null=True)
    category = models.CharField(max_length=255, verbose_name='Category', blank=True, null=True)
    description = models.TextField(max_length=255, verbose_name='Description', blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name='Customer', blank=True, null=True, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, verbose_name='Payment', blank=True, null=True, on_delete=models.CASCADE)
    cart = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Cart')
    daily = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Daily')
    weekly = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Weekly')
    monthly = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='monthly')
    json = models.JSONField(null=True, blank=True, verbose_name='json')
    active = models.BooleanField(verbose_name='active', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    def __str__(self):
        return '{} : {} : {}: {}: {}: {}'.format(self.name, self.category, self.daily, self.weekly, self.monthly, self.active)


class LoginStatistic(models.Model):
    username = models.CharField(max_length=200, verbose_name='Username',null=True, blank=True)
    result = models.CharField(max_length=200, verbose_name='Result',null=True, blank=True)
    ip = models.CharField(max_length=200, verbose_name='IP', null=True, blank=True)
    geopos = models.CharField(max_length=200, verbose_name='Geoposition', null=True, blank=True)
    country_code = models.CharField(max_length=10, verbose_name='Country Code', null=True, blank=True, default='')
    useragent = models.CharField(max_length=200, verbose_name='Useragent', null=True, blank=True)
    device = models.CharField(max_length=200, verbose_name='Device', null=True, blank=True)
    meta = models.TextField(verbose_name='Meta', null=True, blank=True, default=None)
    json = models.JSONField(null=True, blank=True, verbose_name='json', default=dict)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return '{} | {} | {} | {} | {}'.format(self.created_at, self.username, self.result, self.device, self.geopos)


class Wallet(models.Model):
    owner = models.ForeignKey(Customer, verbose_name='Owner', related_name='wallet', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Amount')
    typ = models.CharField(max_length=200, verbose_name='Type')
    description = models.TextField(verbose_name='Description', null=True, blank=True, default=None)
    reference = models.CharField(max_length=555, verbose_name='reference', default='')
    balance = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Balance', blank=True)
    json = models.JSONField(null=True, blank=True, verbose_name='json')
    trash = models.BooleanField(verbose_name='Trash', default=False)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.owner.user.username

    def save(self, *args, **kwargs):
        qs = Wallet.objects.filter(owner=self.owner).first()
        prevbalanse = 0
        if qs:
            prevbalanse = qs.balance
        if self.balance < 0.01:
            self.balance = prevbalanse + decimal.Decimal(self.amount)
        super().save(*args, **kwargs)


class WalletOrder(models.Model):
    STATUS_PENDING_PAYMENT = 'pending_payment'
    STATUS_IN_PROCESSING = 'processing'
    STATUS_CANCELLED = 'cancelled'
    STATUS_COMPLETED = 'completed'
    STATUS_REFUNDET = 'refundet'

    STATUS_CHOICES = (
        (STATUS_PENDING_PAYMENT, 'Pending payment'),
        (STATUS_IN_PROCESSING, 'Processing'),
        (STATUS_CANCELLED, 'Cancelled'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_REFUNDET, 'refundet')
    )

    owner = models.ForeignKey(Customer, verbose_name='Owner', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=19, decimal_places=8, verbose_name='Price')
    fee = models.DecimalField(max_digits=19, default=0, decimal_places=8, verbose_name='Fee')
    total_price = models.DecimalField(max_digits=19, decimal_places=8, verbose_name='Total Price')
    europrice = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Euro Price')
    currency = models.ForeignKey(Currency, verbose_name='Currency', on_delete=models.CASCADE)
    payment_method = models.ForeignKey('Payment', verbose_name='Payment method',
                                       on_delete=models.CASCADE)
    payoption = models.ForeignKey('Payoptions', null=True, blank=True, verbose_name='Payoption', related_name='payopt_worder', on_delete=models.CASCADE)
    status = models.CharField(
        max_length=100,
        verbose_name='Order Status',
        choices=STATUS_CHOICES,
        default=STATUS_PENDING_PAYMENT
    )
    ip = models.CharField(max_length=20, verbose_name='IP Address', null=True, blank=True)
    invoice = models.TextField(verbose_name='invoice', null=True, blank=True)
    postdata = models.TextField(verbose_name='Postdata', null=True, blank=True)
    responsedata = models.TextField(verbose_name='Response data', null=True, blank=True)
    json = models.JSONField(null=True, blank=True, verbose_name='json')
    trash = models.BooleanField(verbose_name='Trash', default=False)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        ordering = ['-pk']

    def save(self, *args, **kwargs):
        
        self.europrice = round(decimal.Decimal(self.total_price / self.currency.price), 2)
        super().save(*args, **kwargs)


class PaymentCallback(models.Model):
    order = models.ForeignKey(Order, verbose_name='Order', related_name='order_callback', on_delete=models.CASCADE, null=True, blank=True)
    worder = models.ForeignKey(WalletOrder, verbose_name='Wallet Order', related_name='worder_callback', on_delete=models.CASCADE, null=True, blank=True)
    data = models.TextField(verbose_name='Data', null=True, blank=True)
    check_order = models.TextField(verbose_name='Check order', null=True, blank=True)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    def __str__(self):
        return str([self.order, self.worder])


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.customer.user.id, filename)


class Verification(models.Model):
    
    customer = models.ForeignKey(Customer, verbose_name='Owner', on_delete=models.CASCADE)
    form_id = models.CharField(max_length=100, verbose_name='Form ID', null=True, blank=True)
    form_url = models.CharField(max_length=500, verbose_name='Form Url', null=True, blank=True)
    verification_id = models.CharField(max_length=500, verbose_name='Verification Id', null=True, blank=True)
    front = models.BinaryField(verbose_name='Front', editable=True, null=True, blank=True)
    second = models.BinaryField(verbose_name='Second', editable=True, null=True, blank=True)
    third = models.BinaryField(verbose_name='Third', editable=True, null=True, blank=True)
    fourth = models.BinaryField(verbose_name='Fourth', editable=True, null=True, blank=True)
    selfie1 = models.BinaryField(verbose_name='Selfie1', editable=True, null=True, blank=True)
    selfie2 = models.BinaryField(verbose_name='Selfie2', editable=True, null=True, blank=True)
    selfie3 = models.BinaryField(verbose_name='Selfie3', editable=True, null=True, blank=True)
    selfie4 = models.BinaryField(verbose_name='Selfie4', editable=True, null=True, blank=True)
    video = models.BinaryField(verbose_name='Video', editable=True, null=True, blank=True)
    status = models.CharField(max_length=20, verbose_name='Status', null=True, blank=True)
    result = models.CharField(max_length=20, verbose_name='Result', null=True, blank=True)
    address = models.BinaryField(verbose_name='Addressproof', editable=True, null=True, blank=True)
    addr_status = models.CharField(max_length=20, verbose_name='Address Status', null=True, blank=True)
    addr_result = models.CharField(max_length=20, verbose_name='Address Result', null=True, blank=True)
    description = models.TextField(verbose_name='Description', null=True, blank=True)
    json = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        ordering = ['-pk']
    
    def __str__(self):
        return str([self.customer, self.status])
        
        
class File(models.Model):

    name = models.CharField(max_length=20, verbose_name='Name', null=True, blank=True)
    description = models.TextField(blank=True, max_length=255, null=True, verbose_name='Description')
    category = models.CharField(max_length=30, verbose_name='Category', null=True, blank=True)
    format = models.CharField(max_length=20, verbose_name='Format', null=True, blank=True)
    size = models.CharField(max_length=20, verbose_name='Size', null=True, blank=True)
    content = models.BinaryField(verbose_name='Content', editable=True, null=True, blank=True)
    hash = models.CharField( max_length=100, verbose_name='Hash', null=True, blank=True)
    path = models.FilePathField(path=None, match=None, max_length=100, null=True, blank=True)
    weburl = models.FilePathField(path=None, match=None, max_length=100, null=True, blank=True)
    json = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    
    def __str__(self):
        return str([self.name, self.description])
    
    
class Jsonfile(models.Model):
    name = models.CharField(max_length=20, verbose_name='Name', null=True, blank=True)
    description = models.TextField(blank=True, max_length=255, null=True, verbose_name='Description')
    category = models.CharField(max_length=30, verbose_name='Category', null=True, blank=True)
    hash = models.CharField( max_length=100, verbose_name='Hash', null=True, blank=True)
    path = models.FilePathField(path=None, match=None, max_length=100, null=True, blank=True, verbose_name='Path')
    weburl = models.FilePathField(path=None, match=None, max_length=100, null=True, blank=True, verbose_name='Weburl')
    json = models.JSONField(null=True, blank=True, verbose_name='json')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    def __str__(self):
        return str([self.name, self.category])


class Message(models.Model):
    name = models.CharField(max_length=20, verbose_name='Name', null=True, blank=True)
    description = models.TextField(blank=True, max_length=255, null=True, verbose_name='Description')
    category = models.CharField(max_length=30, verbose_name='Category', null=True, blank=True)
    text = models.TextField(verbose_name='Text', null=True, blank=True)
    html = models.TextField(verbose_name='Html', null=True, blank=True)
    json = models.JSONField(null=True, blank=True, verbose_name='json')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    def __str__(self):
        return str([self.name, self.category])
    

class Polzov(models.Model):
    fingeprint = models.CharField(max_length=255, verbose_name='FingerPrint', null=True, blank=True, unique=True)
    username = models.CharField(max_length=200, verbose_name='Username', null=True, blank=True)
    anonuser = models.CharField(max_length=200, verbose_name='Anonuser', null=True, blank=True)
    description = models.TextField(blank=True, max_length=255, null=True, verbose_name='Description')
    token = models.CharField(max_length=255, verbose_name='Token', null=True, blank=True)
    hash = models.CharField( max_length=255, verbose_name='Hash', null=True, blank=True)
    uuid = models.CharField( max_length=255, verbose_name='UUID', null=True, blank=True)
    sonstiges = models.CharField( max_length=255, verbose_name='UUID', null=True, blank=True)
    json = models.JSONField(null=True, blank=True, verbose_name='json')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return str([self.username, self.anonuser, self.fingeprint])
    
    
from rest_framework.authtoken.models import Token

class CustomToken(Token):
    fingeprint = models.CharField(max_length=255, verbose_name='fPrint', null=True, blank=True, unique=True)
    json = models.JSONField(null=True, blank=True, verbose_name='json')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return str([self.user, self.fingeprint, self.key])
    
    def save(self, fprint=None, *args, **kwargs):
        
        # print(self.context)
        if fprint: 
            # print(fprint)
            self.fingeprint = fprint
        super().save(*args, **kwargs)
    