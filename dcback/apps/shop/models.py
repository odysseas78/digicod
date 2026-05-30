from pprint import pprint
import uuid, json
from lib.utils.getDatafile import GetDatafile
from decimal import Decimal
from lib.PersistentDictObj import PersistentDictObj
from django.conf import settings
from django.db import models
from apps.accounts.models import Customer
from apps.textchoices import *
from utils.utils import random_code




class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    extra_data = models.JSONField(default=dict, blank=True)

    class Meta:
        abstract = True

class FingPrint(TimeStampedModel):
    fingprint = models.CharField(max_length=255, verbose_name='FingPrint', null=True, blank=True)
    description = models.TextField(blank=True, max_length=255, null=True, verbose_name='Description')
    jdata = models.JSONField(null=True, blank=True, verbose_name='jdata')
    
    def __str__(self):
        return str([self.fingprint, self.description])

class Datafile(TimeStampedModel):
    name = models.CharField(max_length=20, verbose_name='Name', null=True, blank=True)
    description = models.TextField(blank=True, max_length=255, null=True, verbose_name='Description')
    category = models.CharField(max_length=30, verbose_name='Category', null=True, blank=True)
    jdata = models.JSONField(null=True, blank=True, default=dict, verbose_name='jdata')
    
    def __str__(self):
        return str([self.name, self.category])

class Supplier(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name='Supplier', blank=True, null=True)
    supplier_code = models.CharField(max_length=50, choices=SupplierCode.choices, verbose_name="supplier code")
    
    def __str__(self):
        return f'{self.name} {str(self.supplier_code)}'

class Category(TimeStampedModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    api_name=models.CharField(max_length=120)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name="children")

    class Meta:
        ordering = ["name"]
        unique_together = ("parent", "name")

    def __str__(self):
        return self.name

class Brand(TimeStampedModel):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, related_name="brand_supplier", blank=True, null=True)
    category = models.ManyToManyField(Category, related_name="brands", blank=True, null=True)
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    in_stock = models.BooleanField(verbose_name='In stock', default=True)
    image = models.CharField(null=True, blank=True, max_length=255)
    image2 = models.CharField(null=True, blank=True, max_length=255)
    description = models.TextField(verbose_name='Description', null=True, blank=True, default=None)
    active = models.BooleanField(verbose_name='Active', default=False)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    class Meta:
        ordering = ['-pk']
        app_label = "shop"

    def __str__(self):
        return self.title

    @property
    def regions(self):
        brandproducts = self.brand_products.all()
        regs = list({
            region
            for product in brandproducts
            for region in (product.regions or [])
        })
        return regs

    def save(self, *args, **kwargs):
        # if self.id:
        #     if self.active == False:
        #         self.products.all().update(active=False)
        #     if self.active == True:
        #         self.products.filter(qty__gt=0).update(active=True)
            
        #     if self.in_stock == False:
        #         self.products.all().update(in_stock=False)
        #     if self.in_stock == True:
        #         self.products.filter(qty__gt=0).update(in_stock=True)
     
        super().save(*args, **kwargs)

class Product(TimeStampedModel):
    brand = models.ForeignKey(Brand, verbose_name=Brand, related_name='brand_products', on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name="products", default=None, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="product_supplier", blank=True, null=True)
    title = models.CharField(max_length=255, verbose_name='Title', blank=True, null=True)
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
    sku = models.CharField(unique=True, max_length=255, verbose_name='Sku', null=True, default=None)
    slug = models.SlugField(unique=True, null=True, default=None, max_length=255)
    gtin = models.CharField(max_length=255, verbose_name='GTIN', blank=True, null=True, default=None)
    ean = models.CharField(max_length=255, verbose_name='EAN', blank=True, null=True, default=None)
    regions = models.JSONField(max_length=255, verbose_name='Regions', default=dict, blank=True, null=True)
    supplier_product = models.JSONField(verbose_name='supplier_product', default=dict, null=True, blank=True)
    value = models.CharField(max_length=255, verbose_name='Value', null=False, default=None)
    active = models.BooleanField(verbose_name='Active', default=True)
    description = models.TextField(verbose_name='Description', null=True, blank=True, default=None)
    jsondata = models.JSONField(verbose_name='Additional info', default=dict, null=True, blank=True)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return '{} : {} : {} : {} : {}'.format(self.id, self.title, self.brand, self.price, self.regions, self.value)
    
    def save(self, *args, **kwargs):
        self.regions = [
            region.lower()
            for region in self.regions
        ]
        # self.price = Decimal(self.supplier_product.get("stock").get("purchasePrice"))
        # pprint(self.supplier_product)
        # if self.id:
        #     self.brand.in_stock = True if self.brand.products.filter(qty__gt=0).count() > 0 else False
        #     self.brand.save()
        #     self.in_stock = True if self.qty > 0 else False
        #     # if not self.image:s
        #     #     self.image = self.brand.image
        #     ################## Globale profit rate ############################
        #     dbjsonfile = Datafile.objects.filter(name='Shopsettings').first()
        #     shs = PersistentDictObj(dbjsonfile=dbjsonfile, dbjsonfileonly=True)
        #     if not shs.hasattr('Prices'): shs.Prices.ProfitRate = 0
        #     if not shs.hasattr('Prices'): shs.Prices.ProfitRateFix = 0
        #     prate = shs.Prices.ProfitRate
        #     pfix = shs.Prices.ProfitRateFix
        #     ###################################################################
        #     if self.profit > 0:
        #         prate = Decimal(self.profit)
        #     if self.profit_fixed > 0:
        #         pfix = Decimal(self.profit_fixed)
        #     self.price = Decimal(self.pf_price) + Decimal(self.pf_price) * Decimal(prate) / \
        #                 Decimal(100) + Decimal(pfix)
        super().save(*args, **kwargs)

class Cart(TimeStampedModel):

    customer = models.ForeignKey(Customer, verbose_name='Customer', related_name='cart_customer', on_delete=models.CASCADE, null=True, blank=True)
    fingprint = models.ForeignKey(FingPrint, verbose_name='FingPrint', related_name='cart_fingprint', on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField('CartProduct', related_name='cart_products', default=None, verbose_name='Products', null=True, blank=True)
    total_products = models.PositiveIntegerField(default=0)
    payment_method = models.ForeignKey('Payment', null=True, blank=True, verbose_name='Paymentmethod', related_name='cart_pay_method', on_delete=models.CASCADE, default=76)
    payment_method_payment = models.DecimalField(max_digits=9, default=Decimal(0), decimal_places=2, verbose_name='Payment method payment')
    wallet_payment = models.DecimalField(max_digits=9, default=Decimal(0), decimal_places=2, verbose_name='Wallet payment')
    total_price = models.DecimalField(max_digits=9, default=Decimal(0), decimal_places=2, verbose_name='Total price')
    final_price = models.DecimalField(max_digits=9, default=Decimal(0), decimal_places=2, verbose_name='Final price')
    process_fee = models.DecimalField(max_digits=9, default=Decimal(0), decimal_places=2, verbose_name='Processing fee')
    currency = models.ForeignKey('Currency', verbose_name='Currency', related_name='cart_currency', on_delete=models.CASCADE, default=1)
    addinfo = models.JSONField(verbose_name='Additional info', default=dict, null=True, blank=True)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
    
    def save(self, data=None, *args, **kwargs):
        if self.id:
            self.total_products = self.products.count()
            self.total_price = sum([product.final_price  for product in self.products.all()])
            
            subtotal = self.total_price - self.wallet_payment
            subaddfixfee = subtotal + self.payment_method.fee_fix
            self.process_fee = subaddfixfee * (self.payment_method.fee_rate/100) + self.payment_method.fee_fix if subtotal > 0 else 0
            self.final_price = subtotal + self.process_fee if subtotal > 0 else 0
            self.payment_method_payment = self.final_price - self.wallet_payment
        
        super().save(*args, **kwargs)
        
        
        
        
        
        
class CartProduct(TimeStampedModel):

    cart = models.ForeignKey(Cart, verbose_name='Cart', on_delete=models.CASCADE, related_name='cart_cartproduct')
    qty = models.PositiveIntegerField(default=1, verbose_name='Qty')
    product = models.ForeignKey(Product, verbose_name='Product', related_name='product', on_delete=models.CASCADE, unique=True)
    title = models.CharField(max_length=250, verbose_name='title')
    product_codes = models.ManyToManyField('ProductCode', blank=True, related_name='related_cart_productproduct_codes')
    item_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Cart Product Price')
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Total Price')
    deleted = models.BooleanField(verbose_name='Deleted', default=False)


    class Meta:
        ordering = ['-pk']

    def __str__(self):
        if self.title:
            return "Cartproduct: {}".format(self.title)
        else:
            return "Cartproduct: {}".format(self.product.title)

    def save(self, *args, **kwargs):
        if self.id:
            self.title = self.product.title
            self.item_price = self.product.price
            self.final_price = self.item_price * self.qty
        super().save(*args, **kwargs)

class ProductCode(models.Model):
    uuid = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    cart_product = models.ForeignKey(CartProduct, verbose_name='CartProduct', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name='Cart', on_delete=models.CASCADE)
    supplier_order_id = models.CharField(max_length=255, verbose_name='PF order Reference')
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

class Currency(TimeStampedModel):
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

    class Meta:
        ordering = ['-type','pk']

    def __str__(self):
        return '{} : {} : {}'.format(self.shortname, self.created_at, self.updated_at)

    def save(self, *args, **kwargs):
        shopsettings = GetDatafile("Shopsettings")
        if not shopsettings.has('currency_exchange_rate'): shopsettings.currency_exchange_rate = 0
        
        glrate = shopsettings.currency_exchange_rate
        if self.shortname != 'EUR':
            if self.fee_rate > 0:
                self.price = Decimal(self.orig_price) + Decimal(self.orig_price) * \
                            Decimal(self.fee_rate) / Decimal(100)
            else:
                self.price = Decimal(self.orig_price) + Decimal(self.orig_price) * \
                            Decimal(glrate) / Decimal(100)
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

class Payoptions(TimeStampedModel):
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
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    def __str__(self):
        return '{} : {} : {}'.format(self.name, self.payment_method.name, self.enabled)

class Payment(TimeStampedModel):
    type = models.CharField(max_length=255, verbose_name='Type', null=True, blank=True)
    provider = models.CharField(max_length=255, verbose_name='Payment Provider', default=None, null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='Payment Name')
    payoptions = models.ManyToManyField(Payoptions, verbose_name='payoptions', related_name='pay_options', blank=True)
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
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    def __str__(self):
        return '{} : {} : {}'.format(self.name, self.fee_rate, self.fee_fix)

class Limit(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name='Name', blank=True, null=True)
    category = models.CharField(max_length=255, verbose_name='Category', blank=True, null=True)
    description = models.TextField(max_length=255, verbose_name='Description', blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name='Customer', blank=True, null=True, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, verbose_name='Payment', blank=True, null=True, on_delete=models.CASCADE)
    cart = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Cart')
    daily = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Daily')
    weekly = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Weekly')
    monthly = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='monthly')
    active = models.BooleanField(verbose_name='active', default=False)
    deleted = models.BooleanField(verbose_name='Deleted', default=False)

    def __str__(self):
        return '{} : {} : {}: {}: {}: {}'.format(self.name, self.category, self.daily, self.weekly, self.monthly, self.active)

# class Cart(TimeStampedModel):
#     customer = models.ForeignKey(CustomerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="carts")
#     session_key = models.CharField(max_length=64, blank=True, db_index=True)

#     def __str__(self):
#         return self.customer.email if self.customer else self.session_key or f"cart-{self.pk}"

#     @property
#     def total_amount(self):
#         return sum((item.line_total for item in self.items.select_related("partner_product")), Decimal("0.0000"))


# class CartItem(TimeStampedModel):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
#     partner_product = models.ForeignKey(PartnerProduct, on_delete=models.CASCADE, related_name="cart_items", null=True, blank=True)
#     quantity = models.PositiveIntegerField(default=1)
#     payment_method = models.DecimalField(max_digits=12, decimal_places=4)

#     class Meta:
#         unique_together = ("cart", "partner_product")

#     @property
#     def line_total(self):
#         if not self.partner_product:
#             return Decimal("0.0000")
#         return self.partner_product.retail_price * self.quantity


# class CustomerOrder(TimeStampedModel):
#     class Status(models.TextChoices):
#         PENDING = "pending", "Pending"
#         PROCESSING = "processing", "Processing"
#         COMPLETED = "completed", "Completed"
#         FAILED = "failed", "Failed"

#     number = models.CharField(max_length=32, unique=True, editable=False)
#     customer = models.ForeignKey(CustomerProfile, on_delete=models.PROTECT, related_name="orders")
#     cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
#     status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
#     total_amount = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal("0.0000"))
#     currency = models.CharField(max_length=10, default="EUR")
#     failure_reason = models.TextField(blank=True)
#     raw_payload = models.JSONField(default=dict, blank=True)

#     class Meta:
#         ordering = ["-created_at"]

#     def __str__(self):
#         return self.number

#     def save(self, *args, **kwargs):
#         if not self.number:
#             self.number = uuid.uuid4().hex[:12].upper()
#         super().save(*args, **kwargs)




# class Partner(TimeStampedModel):
#     name = models.CharField(max_length=120)
#     code = models.SlugField(max_length=60, unique=True)
#     base_url = models.URLField(blank=True)
#     is_active = models.BooleanField(default=True)
#     settings = models.JSONField(default=dict, blank=True)

#     class Meta:
#         ordering = ["name"]

#     def __str__(self):
#         return self.name


# class PartnerApiToken(TimeStampedModel):
#     partner = models.OneToOneField(Partner, on_delete=models.CASCADE, related_name="api_token")
#     token = models.CharField(max_length=512)
#     valid_until = models.DateTimeField()

#     def __str__(self):
#         return f"{self.partner.code} token"


# class Product(TimeStampedModel):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(max_length=255, unique=True)
#     brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products", null=True, blank=True)
#     category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", null=True, blank=True)
#     description = models.TextField(blank=True)
#     image_url = models.URLField(blank=True)
#     face_value_amount = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal("0.0000"))
#     face_value_currency = models.CharField(max_length=10, blank=True)
#     is_active = models.BooleanField(default=True)
#     raw_payload = models.JSONField(default=dict, blank=True)

#     class Meta:
#         ordering = ["name"]

#     def __str__(self):
#         return self.name


# class PartnerProduct(TimeStampedModel):
#     partner = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name="product_offers")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="partner_offers")
#     external_id = models.CharField(max_length=120)
#     sku = models.CharField(max_length=120)
#     currency = models.CharField(max_length=10, default="EUR")
#     cost_price = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal("0.0000"))
#     retail_price = models.DecimalField(max_digits=12, decimal_places=4, default=Decimal("0.0000"))
#     available_stock = models.PositiveIntegerField(default=0)
#     delivery_type = models.CharField(max_length=50, blank=True)
#     product_type = models.CharField(max_length=50, blank=True)
#     countries = models.JSONField(default=list, blank=True)
#     languages = models.JSONField(default=list, blank=True)
#     platforms = models.JSONField(default=list, blank=True)
#     is_active = models.BooleanField(default=True)
#     raw_payload = models.JSONField(default=dict, blank=True)
#     extra_attributes = models.JSONField(default=dict, blank=True)

#     class Meta:
#         ordering = ["product__name", "sku"]
#         unique_together = ("partner", "sku")

#     def __str__(self):
#         return f"{self.partner.code}:{self.sku}"


# class CustomerProfile(TimeStampedModel):
#     class AccountType(models.TextChoices):
#         REGISTERED = "registered", "Registered"
#         GUEST = "guest", "Guest"

#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_profile")
#     account_type = models.CharField(max_length=20, choices=AccountType.choices, default=AccountType.GUEST)

#     def __str__(self):
#         return self.user.email or self.user.username

#     @property
#     def email(self):
#         return self.user.email
    
# class FingPrint(TimeStampedModel):
#     fingprint = models.CharField(max_length=255, verbose_name='FingerPrint', unique=True, null=True, blank=True)