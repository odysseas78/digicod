from django.contrib.auth.models import User
from rest_framework import serializers
from apps.priceConverter import GlobalDecimalSerializer
from .models import Brand, Cart, Category, Currency, Payment, Product, Limit, CartProduct
from decimal import Decimal, ROUND_HALF_UP
from rest_framework import serializers



def make_serializer(model, fields=None, exclude=None, extra_fields=None):
    extra_fields = extra_fields or {}

    meta_attrs = {
        "model": model,
    }

    if fields is not None:
        meta_attrs["fields"] = fields
    elif exclude is not None:
        meta_attrs["exclude"] = exclude
    else:
        meta_attrs["fields"] = "__all__"

    Meta = type("Meta", (), meta_attrs)

    attrs = {
        "Meta": Meta,
        **extra_fields,
    }

    return type("DynamicProductSerializer", (serializers.ModelSerializer,), attrs)



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent_id")
        
        
class BrandSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Brand
        fields = ["id","title","slug","in_stock","image","image2","description","category","regions"]
        

class ProductSerializer(GlobalDecimalSerializer):
    
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(many=True, read_only=True)
    # price = price = ConvertedPriceField(
    #     max_digits=10,
    #     decimal_places=2,
    #     read_only=True,
    # )
    class Meta:
        model = Product
        fields = ["title", "image", "id", "price","description","regions", "qty","in_stock","brand", "category","value"]
        exclude = None
        # fields = '__all__'

class PaymentSerializer(GlobalDecimalSerializer):
    # items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        exclude = ["type","provider","enabled","json","created_at", "updated_at","extra_data","html"]

class CurrencySerializer(serializers.ModelSerializer):
    # items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Currency
        fields = ["id","longname","shortname","price","sign","image", "image2","svg","html"]
        
class CartProductSerializer(GlobalDecimalSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartProduct
        exclude = ["created_at", "updated_at","extra_data"]


class CartSerializer(GlobalDecimalSerializer):
    currency = CurrencySerializer(read_only=True)
    payment_method = PaymentSerializer(read_only=True)
    products = CartProductSerializer(many=True)
       
    
    class Meta:
        model = Cart
        exclude = ("updated_at", "created_at", "extra_data","for_anonymous_user", "fingprint", "addinfo")
        



# class AddCartItemSerializer(serializers.Serializer):
#     partner_product_id = serializers.PrimaryKeyRelatedField(
#         queryset=PartnerProduct.objects.filter(is_active=True, partner__is_active=True, product__is_active=True)
#     )
#     quantity = serializers.IntegerField(min_value=1, default=1)


# class CheckoutSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     first_name = serializers.CharField(max_length=120)
#     last_name = serializers.CharField(max_length=120)
#     create_account = serializers.BooleanField(default=False)
#     password = serializers.CharField(max_length=128, required=False, allow_blank=False, write_only=True)

#     def validate(self, attrs):
#         if attrs.get("create_account") and not attrs.get("password"):
#             raise serializers.ValidationError({"password": "Password is required when create_account is true."})
#         return attrs


# class DeliveredCodeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DeliveredCode
#         fields = ("code", "serial", "image_url", "code_type")


# class CustomerOrderItemSerializer(serializers.ModelSerializer):
#     codes = DeliveredCodeSerializer(many=True, read_only=True)

#     class Meta:
#         model = CustomerOrderItem
#         fields = (
#             "id",
#             "product_name",
#             "product_sku",
#             "quantity",
#             "unit_price",
#             "line_total",
#             "supplier_delivery_type",
#             "codes",
#         )


class CustomerSerializer(serializers.ModelSerializer):
    account_type = serializers.CharField(source="customer_profile.account_type", read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "account_type")


# class CustomerOrderSerializer(serializers.ModelSerializer):
#     items = CustomerOrderItemSerializer(many=True, read_only=True)
#     customer = CustomerSerializer(source="customer.user", read_only=True)

#     class Meta:
#         model = CustomerOrder
#         fields = (
#             "id",
#             "number",
#             "status",
#             "customer",
#             "total_amount",
#             "currency",
#             "failure_reason",
#             "items",
#             "created_at",
#         )
