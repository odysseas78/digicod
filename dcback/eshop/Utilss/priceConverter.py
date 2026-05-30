from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from rest_framework import serializers
from django.db.models import Q, Avg, Count, Min, Sum, F
from lib.PersistentDictObj import PersistentDictObj
from eshop.models import Basket

try:
    from http.cookies import SimpleCookie
except ImportError:
    from Cookie import SimpleCookie # type: ignore


def getCookies(request):
    cookies = SimpleCookie(request.headers.get('set-cookie'))
    polz = request.COOKIES.get('_polz') if request.COOKIES.get('_polz') else cookies.get('_polz').value if cookies.get('_polz') else None
    ccc = request.COOKIES.get('_ccc') if request.COOKIES.get('_ccc') else cookies.get('_ccc').value if cookies.get('_ccc') else None
    return {'polz':polz, 'ccc':ccc}

class ConvertedPriceField(serializers.DecimalField):
    """
    Gibt Preisfelder nicht roh aus, sondern konvertiert.
    Beispiel: EUR -> THB
    """

    def to_representation(self, value):
        if value is None:
            return None
        if self.context.get('request').user.is_authenticated:
            basket = self.context.get('request').user.customer.basket.filter(in_order=False).filter(
                     Q(fingprint=getCookies(self.context.get('request')).get('polz')) | Q(id=getCookies(self.context.get('request')).get('ccc'))
                     ).first()
        else:
            basket = Basket.objects.filter(in_order=False).filter(
                     Q(fingprint=getCookies(self.context.get('request')).get('polz')) | Q(id=getCookies(self.context.get('request')).get('ccc'))
                     ).first()


        value = Decimal(value)

         # Beispielkurs
        rate = basket.currency.price

        converted = (value * rate).quantize(
               Decimal("0.01"),
               rounding=ROUND_HALF_UP
         )
        return str(converted)
      #   return {
      #       "original": str(value),
      #       "original_currency": "EUR",
      #       "converted": str(converted),
      #       "converted_currency": cur.shortname,
      #    }


class BasePriceModelSerializer(serializers.ModelSerializer):
    PRICE_FIELD_NAMES = {
        "price",
        "sale_price",
        "gross_price",
        "net_price",
        "unit_price",
    }

    def build_standard_field(self, field_name, model_field):
        field_class, field_kwargs = super().build_standard_field(field_name, model_field)

        # Nur DecimalFields, die Preisfelder sind
        if isinstance(model_field, models.DecimalField) and field_name in self.PRICE_FIELD_NAMES:
            field_class = ConvertedPriceField
      

        return field_class, field_kwargs
     
     
class GlobalDecimalSerializer(serializers.ModelSerializer):
    serializer_field_mapping = (
        serializers.ModelSerializer.serializer_field_mapping.copy()
    )
    serializer_field_mapping[models.DecimalField] = ConvertedPriceField