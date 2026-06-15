from typing_extensions import Required
from rest_framework import serializers
import os
import django

from eshop.PrepaidForge.Order import get_pf_balance
from eshop_api.main.serializers import PaymentSerializer

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from eshop.models import Currency, Limit, Order, PaymentCallback, Polzov, WalletOrder, Customer, \
     Brand, Product, Category, CartProduct, Cart, ProductCode, Wallet
from eshop.serializers import CustomersSerializer, CurrencySerializer, UsersSerializer
from eshop_api.cart.serializers import CartSerializer
from apps.accounts.models import *

class CustomerSerializer(serializers.ModelSerializer):

    user = UsersSerializer(required=False)

    class Meta:
        model = Customer
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    
    category=CategorySerializer(required=False, many=True)

    class Meta:
        model = Brand
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    class Meta:
        model = Product
        fields = '__all__'
        
        
class ProductCodesSerializer(serializers.ModelSerializer):
    # brand = BrandSerialaizer()
    class Meta:
        model = ProductCode
        fields = '__all__'
        

class Orders3Serializer(serializers.ModelSerializer):
    cart = CartSerializer(required=False)
    customer = CustomerSerializer(required=False)
    # customer = serializers.ReadOnlyField(source='customer.user.username', read_only=True)
    pay_currency = CurrencySerializer(required=False)
    class Meta:
        model = Order
        fields = '__all__'


class CartsSerializer(serializers.ModelSerializer):
    order = Orders3Serializer()
    owner = CustomerSerializer()
    class Meta:
        model = Cart
        fields = '__all__'
        
        
class CartProductSerializer(serializers.ModelSerializer):
    cart = CartsSerializer()
    product = ProductSerializer()
    product_codes = ProductCodesSerializer(many=True)
    
    # order__status = CartSerializer('order__status')
    class Meta:
        model = CartProduct
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    owner = CustomerSerializer()
    class Meta:
        model = Wallet
        fields = '__all__'


class PaymentCallbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentCallback
        fields = '__all__'


class LimitsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Limit
        fields = '__all__'



class PolzovSerializer(serializers.ModelSerializer):

    user = UsersSerializer(required=False)

    class Meta:
        model = Polzov
        fields = '__all__'


class WordersSerializer(serializers.ModelSerializer):
    owner=CustomerSerializer(required=False)
    currency=CurrencySerializer(required=False)
    payment_method=PaymentSerializer(required=False)

    class Meta:
        model = WalletOrder
        extra_kwargs = {'price': {'required': False}, 'total_price': {'required': False}, 'europrice': {'required': False}, 
                        'client': {'required': False}, 'client': {'required': False}, 'client': {'required': False}}
        fields = '__all__'



class OrdersSerializer(serializers.ModelSerializer):

    # customer = CustomersSerializer()
    cart = CartSerializer(required=False)
    customer = CustomerSerializer(required=False)
    # customer = serializers.ReadOnlyField(source='customer.user.username', read_only=True)
    order_callback = PaymentCallbackSerializer(many=True, required=False)
    pay_currency = CurrencySerializer(required=False)
    # currency_name = serializers.ReadOnlyField(source='pay_currency.shortname', read_only=True)
    # currency_type = serializers.ReadOnlyField(source='pay_currency.type', read_only=True)
    # final_price = serializers.SerializerMethodField()

    def get_final_price(self, obj):
        dg = 8
        if obj.pay_currency.type == 'fiat':
            dg = 2
        return str(round(obj.cart.order_final_price * obj.pay_currency.price, dg))

    class Meta:
        model = Order
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     # First call the __init__ method of super class
    #     super(OrdersSerializer, self).__init__(*args, **kwargs)

    #     if 'context' in kwargs:
    #         if 'request' in kwargs['context']:
    #             if kwargs['context']['request'].query_params.get('s') == None:
    #                 exclude = ['comment', 'del_email','ip','order_date','postdata',
    #                            'responsedata', 'cart', 'pay_currency']
    #                 for other in exclude:
    #                     self.fields.pop(other)
    #             if kwargs['context']['request'].query_params.get('s') != None:
    #                 exclude = ['currency_name', 'currency_type', 'final_price']
    #                 for other in exclude:
    #                     self.fields.pop(other)
    #                 self.fields['customer'] = CustomersSerializer()
    #                 self.fields['cart'] = CartSerializer()


class OrdersSerializerLight(serializers.ModelSerializer):

    # customer = CustomersSerializer()
    # cart.final_price = CartSerializer()
    cart_final_price = serializers.ReadOnlyField(source='cart.final_price', read_only=True)
    # customer_username = serializers.ReadOnlyField(source='customer.user.username', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        # fields = ['created_at', 'id', 'status', 'customer', 'cart_final_price']


import jsons
from django.db.models import Q, Sum

from eshop.models import Order, WalletOrder, Cart, CartProduct, Wallet, Customer
from django.core import serializers as SeriaLizer

qs={'order': Order.objects.all(), 'worder': WalletOrder.objects.all(), 'cart': Cart.objects.all(), 'cp': CartProduct.objects.all(),
    'wallet': Wallet.objects.all(), 'customer': Customer.objects.all()}


def pay_method_amounts(date_from='2000-01-01 22:22:00+00', date_to='3000-01-01 22:22:00+00'):

    if date_from == None:
        date_from = '2000-01-01 22:22:00+00'
    if date_to == None:
        date_to = '3000-01-01 22:22:00+00'
    a = ('created_at__gt',date_from)
    b = ('created_at__gt', date_to)
    all_orders = qs['order'].filter(Q(status='completed') | Q(status='refunded')).filter(a).exclude(b)
    all_worders = qs['worder'].filter(status='completed').filter(a).exclude(b)
    opm = set(all_orders.values_list('cart__payment_method__name', flat=True))
    wpm = set(all_worders.values_list('payment_method__name', flat=True))
    pay_mets = opm | wpm
    pay_meth_totals = []
    for item in pay_mets:
        pay_meth = {}
        osumqs = all_orders.filter(cart__payment_method__name=item)
        osum = osumqs.aggregate(Sum('cart__payment_method_payment'))['cart__payment_method_payment__sum']
        if osum == None:
            osum = 0
        wsumqs = all_worders.filter(payment_method__name=item)
        pay_meth['name'] = item
        # pay_meth['amount'] = sum([osumqs.cart.payment_method_payment for osumqs in osumqs])
        pay_meth['amount'] = 0
        pay_meth['amount'] += round(sum([(wsumqs.total_price / wsumqs.currency.price) for wsumqs in wsumqs]),2) + osum
        if item == 'Wallet':
            pay_meth['amount'] += osumqs.aggregate(Sum('cart__wallet_payment'))['cart__wallet_payment__sum']\
            - osumqs.aggregate(Sum('cart__refund_amount'))['cart__refund_amount__sum']
        pay_meth_totals.append(pay_meth)
    if all_orders:
        orders_amount = all_orders.aggregate(Sum('cart__final_price'))['cart__final_price__sum']\
        - all_orders.aggregate(Sum('cart__refund_amount'))['cart__refund_amount__sum']
    else:
        orders_amount = 0
    worders_amount = round(sum([(all_worders.price / all_worders.currency.price) for all_worders in all_worders]),2)
    # all_orders.cart.products.product
    return {'popul_brands': popul_brands(all_orders),'pay_meth_totals': pay_meth_totals, 'orders_amount': orders_amount, 'worders_amount': worders_amount}


def popul_brands(all_orders):
    # all_orders = qs['order'].filter(Q(status='completed') | Q(status='refunded'))
    brandsqs = all_orders.values_list('cart__products__product__brand__title', flat=True)
    brands = set(brandsqs)
    popul_brands = []
    for brand in brands:
        try:
            brand_orders = all_orders.filter(cart__products__product__brand__title=brand)
            brandsum = brand_orders.aggregate(Sum('cart__products__final_price'))['cart__products__final_price__sum']
            SeriaLizer.serialize('json', [brand_orders.first().cart.products.first().product.brand])
            jsn = SeriaLizer.serialize('json', [brand_orders.first().cart.products.first().product.brand])
            popul_brands.append([brandsum,{'brandsum': brandsum},jsons.loads(jsn)])
        except Exception as d:
            continue   
    popul_brands.sort()
    popul_brands.reverse()

    return popul_brands

# print(popul_brands())
# print(popul_brands('2000-01-01 22:22:00+00','3000-01-01 22:22:00+00'))
# qs = qs['order'].filter(Q(status='completed') | Q(status='refunded'))\
#            .values_list('cart__products__product__brand__title', 'cart__products__final_price')\
#       .filter(cart__products__product__brand__title='Bitnovo')
# qsg = qs['order'].filter(Q(status='completed') | Q(status='refunded'))
# print(qsg.aggregate(Sum('cart__products__final_price'))['cart__products__final_price__sum']
#       - qsg.aggregate(Sum('cart__refund_amount'))['cart__refund_amount__sum'])
# all_orders = qs['order'].filter(Q(status='completed') | Q(status='refunded')).filter(created_at__gt='2022-03-14 17:22:00')\
#     .filter(cart__products__product__brand__title='Bitnovo').distinct()
# all_orders = qs['order'].filter(Q(status='completed') | Q(status='refunded')).filter(created_at__gt='2022-03-14 17:22:00').annotate(sum('cart.final_price'))
# print(all_orders)

# print(sum([all_orders.cart.cartproduct.final_price for all_orders in all_orders]))

def wallet_balance(userid=0):
    if userid == 0:
        wb = 0
        for a in qs['customer'].exclude(rolle='s_customer'):
            wb += qs['wallet'].filter(owner=a).first().balance
        try:
            pfb = round(get_pf_balance()['amount'],2)
        except Exception as d:
            print(d)
            pfb = None
        return {'wallet_balance':wb, 'pf_balance': pfb}
    else:
        return qs['wallet'].filter(owner=userid).first().balance

# print(wallet_balance())

def view_model(model):
    jsn = SeriaLizer.serialize('json', qs[model], indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True)
    jsn2 = SeriaLizer.serialize('json', qs['cart'], indent=2, use_natural_foreign_keys=True,
                               use_natural_primary_keys=True)
    return [jsons.loads(jsn), jsons.loads(jsn2)]

# print(SeriaLizer.serialize('json',list(qs['order'].values('cart')), indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True))
# res = qs['order'].first()
# print(jsons.dumps(qs['order'].cart))
# print(DictObj(res))
# qd = oc.filter(pk=857551).first()
# userorders = allobj['order'].filter(cart=allobj['cart'].filter(in_order=True).last())

# orderser = SeriaLizer.serialize('json', allobj['order'], indent=2, use_natural_foreign_keys=False, use_natural_primary_keys=False)
# print(set(qs['worder'].values_list('payment_method__name', flat=True)))