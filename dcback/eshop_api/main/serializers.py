import os
import sys

from eshop.models import Payoptions, Product, Category, CartProduct, Brand, Payment, Currency, ProductCode, Verification
from eshop.Utilss.PriceRabatt import RabattCeck
from rest_framework import serializers


# class CryptoAddressSerializer(serializers.ModelSerializer):

#     # currency = CurrencySerializer()
#     # network = CryptoNetworkSerializer()

#     class Meta:
#         model = CryptoAddress
#         fields = ['id','currency', 'address','network','description']

# class CryptoNetworkSerializer(serializers.ModelSerializer):

#     address = CryptoAddressSerializer()

#     class Meta:
#         model = CryptoNetwork
#         fields = ['id','currency','shortname','longname', 'address','description']


class CurrencySerializer(serializers.ModelSerializer):
    # network = CryptoNetworkSerializer(many=True)

    class Meta:
        model = Currency
        # fields = '__all__'
        exclude = ['orig_price', 'fee_rate']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Brand
        # read_only = True
        fields = '__all__'
        read_only_fields = ['title', 'slug', 'description', 'image', 'image2', 'imagepf', 'api_title', 'in_stock']


class BrandsSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=True)

    class Meta:
        model = Brand
        # read_only = True
        fields = '__all__'

    def to_representation(self, instance):
        self.fields['category'] = CategorySerializer(many=True)
        return super(BrandsSerializer, self).to_representation(instance)



class ProductSerializer(serializers.ModelSerializer):

    # category = CategorySerializer()
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = ['id', 'title', 'image', 'brand', 'price', 'in_stock', 'qty', 'sku', 'slug', 'region', 'currency', 'value', 'active']
        # exclude = ['users']
        read_only_fields = ['id', 'title', 'image', 'brand', 'in_stock', 'price', 'qty', 'sku', 'slug', 'region', 'currency', 'value', 'active']


class ProductsSerializer(serializers.ModelSerializer):

    # category = CategorySerializer()
    # brand = BrandsSerializer()

    class Meta:
        model = Product
        fields = '__all__'


class CustomBrandsSerializer(BrandsSerializer):

    products = serializers.SerializerMethodField()

    @staticmethod
    def get_products(obj):
        return ProductsSerializer(Product.objects.filter(brand=obj), many=True).data


class CustomBrandSerializer(BrandSerializer):

    products = serializers.SerializerMethodField()

    @staticmethod
    def get_products(obj):
        return ProductSerializer(Product.objects.filter(brand=obj), many=True).data


class CustomCategorySerializer(CategorySerializer):

    brands = serializers.SerializerMethodField()

    @staticmethod
    def get_brands(obj):
        return BrandSerializer(Brand.objects.filter(category=obj, active=True), many=True).data


class ProductCodeSerializer(serializers.ModelSerializer):

    # cart = CartSerializer()
    # ct_product = CartProductSerializer()
    # order = OrderSerializer()

    class Meta:
        model = ProductCode
        # fields = ('ct_product', 'cart', 'order', 'order_id', 'code', 'serial')
        fields = '__all__'


class CartProductSerializer(serializers.ModelSerializer):

    product = ProductSerializer()
    currency = CurrencySerializer()
    product_codes = ProductCodeSerializer(many=True)
    # rabatt = serializers.SerializerMethodField()

    # def get_rabatt(self, obj):
    #     rch = RabattCeck(obj)
    #     return rch.cp_check()

    class Meta:
        model = CartProduct
        fields = '__all__'
        # fields = ['id', 'product', 'qty', 'final_price']


class PayoptionsSerializer(serializers.ModelSerializer):

    # cart = CartSerializer()
    # ct_product = CartProductSerializer()
    # order = OrderSerializer()

    class Meta:
        model = Payoptions
        # fields = ('ct_product', 'cart', 'order', 'order_id', 'code', 'serial')
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    prom_fee = serializers.SerializerMethodField()
    currencies = CurrencySerializer(many=True)
    payoptions = PayoptionsSerializer(many=True)

    def get_prom_fee(self, obj):
        from eshop.models import Jsonfile
        if self.context.get('request') and not self.context.get('request').user.is_anonymous:
            if self.context.get('request').user.customer.rolle == 'promneo':
                data = Jsonfile.objects.filter(name='Shopsettings').first().json
                return data.get('Prices').get('PromNeo%')

    class Meta:
        model = Payment
        fields = '__all__'



class VerificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Verification
        fields = '__all__'
        # fields = ['id', 'product', 'qty', 'final_price']