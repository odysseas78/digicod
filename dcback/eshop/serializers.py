from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from eshop.models import Customer, Wallet, WalletOrder
from eshop_api.cart.serializers import OrderSerializer
from eshop_api.main.serializers import PaymentSerializer, CurrencySerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from djoser.serializers import TokenCreateSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate
from djoser.conf import settings
from rest_framework.viewsets import ModelViewSet

class CustomTokenCreateSerializer(TokenCreateSerializer):
    
    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        if self.user and not self.user.is_active:
            self.fail("inactive_account")
        if self.user and self.user.is_active:
            return attrs
        self.fail("invalid_credentials")


class CustomersSerializer(serializers.ModelSerializer):

    # user = UsersSerializer()
    # orders = OrderSerializer(many=True)

    class Meta:
        model = Customer
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    customer = CustomersSerializer()

    def update(self, instance, validated_data):
        customer = validated_data.get('customer')
        instance.__dict__.update(validated_data)
        if customer:
            instance.customer.__dict__.update(customer)
            instance.customer.save()
        instance.save()
        return instance

    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login']
        # exclude = ['password']


class CustomerSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        # fields = '__all__'
        exclude = ['ip','limit','limit_reset','rolle', 'status']


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')
        # extra_kwargs = {
        #     'first_name': {'required': False},
        #     'last_name': {'required': False}
        # }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            # first_name=validated_data['first_name'],
            # last_name=validated_data['last_name'],
            is_active=False
        )

        user.set_password(validated_data['password'])
        user.save()
        customer = Customer.objects.create(
            user=user,
            rolle='new',
            status='Unverified'
        )
        customer.save()
        Wallet.objects.create(
            owner=user.customer,
            balance=0
        )

        return user


class WalletSerializer(serializers.ModelSerializer):
    # owner = CustomersSerializer()

    class Meta:
        model = Wallet
        fields = '__all__'


class WalletOrdersSerializer(serializers.ModelSerializer):

    # currency = CurrencySerializer()
    # payment_method = PaymentSerializer()
    # crypto_address = CryptoAddressSerializer()
    currency_name = serializers.ReadOnlyField(source='currency.shortname', read_only=True)
    # currency_price = serializers.ReadOnlyField(source='currency.price', read_only=True)
    # payment_method_name = serializers.ReadOnlyField(source='payment_method.name', read_only=True)
    # username = serializers.ReadOnlyField(source='owner.user.username', read_only=True)

    class Meta:
        model = WalletOrder
        fields = '__all__'
        # exclude = ['payment_method', 'crypto_address','currency','responsedata','postdata']

    # def __init__(self, *args, **kwargs):
    #     # First call the __init__ method of super class
    #     super(WalletOrdersSerializer, self).__init__(*args, **kwargs)

    #     if 'context' in kwargs:
    #         if 'request' in kwargs['context']:
    #             if kwargs['context']['request'].query_params.get('s') == None:
    #                 exclude = ['payment_method', 'responsedata','postdata']
    #                 for other in exclude:
    #                     self.fields.pop(other)
    #             if kwargs['context']['request'].query_params.get('s') != None:
    #                 self.fields['owner'] = CustomersSerializer()
    #                 self.fields['payment_method'] = PaymentSerializer()
    #                 self.fields['currency'] = CurrencySerializer()
                    
                    
class WalletOrderSerializer(serializers.ModelSerializer):

    # currency = CurrencySerializer()
    # payment_method = PaymentSerializer()
    class Meta:
        model = WalletOrder
        # fields = '__all__'
        # exclude = ['ip', 'invoice','postdata']


