from eshop.models import Cart, Order
from eshop.models import Customer
from eshop_api.main.serializers import CartProductSerializer, PaymentSerializer, CurrencySerializer
from eshop.Utilss.PriceRabatt import RabattCeck
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):

    user = serializers.SerializerMethodField()
    # user = UserSerializer
    class Meta:
        model = Customer
        # fields = '__all__'
        exclude = ['ip', 'rolle', 'status']

    @staticmethod
    def get_user(obj):
        if not (obj.user.first_name and obj.user.last_name):
            return obj.user.username
        return ' '.join([obj.user.first_name, obj.user.last_name])



class CartSerializer(serializers.ModelSerializer):

    products = CartProductSerializer(many=True)
    # owner = CustomerSerializer()
    payment_method = PaymentSerializer()
    limit = serializers.SerializerMethodField()
    # rabatt = serializers.SerializerMethodField()

    def get_limit(self, obj):
        res = False
        if obj.final_price > 500:
            res = True
        return res
    
    # def get_rabatt(self, obj):
    #     rch = RabattCeck(obj)
    #     return rch.check().get('summ')

    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    customer = CustomerSerializer()
    cart = CartSerializer()
    pay_currency = CurrencySerializer()
    final_price = serializers.SerializerMethodField()

    def get_final_price(self, obj):
        if obj.pay_currency.type == 'crypto':
            if obj.pay_currency.shortname == 'USDT':
                tofix = 2
            else:
                tofix = 8
        else:
            tofix = 2
        return str(round(obj.cart.order_final_price * obj.pay_currency.price, tofix))

    class Meta:
        model = Order
        # fields = '__all__'
        exclude = ['postdata', 'invoice']



