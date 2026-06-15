from django.shortcuts import get_object_or_404
from eshop.models import Cart, Product, CartProduct, Customer, Currency, Payment, Wallet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from loguru import logger
from .serializers import CartSerializer
import requests
import json

class CartViewSet(ModelViewSet):

    # permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    @staticmethod
    def get_cart(request):
        
        if request.user.is_authenticated:
            cart = Cart.objects.filter(owner=request.user.customer, for_anonymous_user=False, in_order=False).first()
            if not cart:
                payment = Payment.objects.all().first()
                cart = Cart.objects.create(
                    owner=request.user.customer,
                    for_anonymous_user=False,
                    payment_method=payment
                )
                cart.save()
                return cart
            return cart
        gast_cart = request.COOKIES.get('_ccc')
        if gast_cart and gast_cart != 'undefined':
            cart = Cart.objects.filter(id=gast_cart, for_anonymous_user=True, in_order=False).first()
            if cart:
                return cart
        payment = Payment.objects.all().first()
        cart = Cart.objects.create(
            # owner=request.user.customer,
            for_anonymous_user=True,
            payment_method=payment
        )
        cart.save()
        return cart




    @staticmethod
    def _get_or_create_cart_product(customer: Customer, cart: Cart, product: Product, qty):
        # if customer.user:
        cart_product, created = CartProduct.objects.get_or_create(
            user=customer,
            product=product,
            cart=cart,
            defaults={
                "qty":qty
            }
        )
        return cart_product, created

    @action(methods=["get"], detail=False)
    def current_customer_cart(self, *args, **kwargs):
        cart = self.get_cart(self.request)
        cart_serializer = CartSerializer(cart)
        response = Response(cart_serializer.data)
        # if cart.for_anonymous_user == True:
        #     response.set_cookie('_ccc', cart.id,  samesite=None, httponly=False, max_age=None, expires=None, path='/', domain=None, secure=True)
        return response

    @action(methods=['put'], detail=False, url_path='current_customer_cart/add_to_cart/(?P<product_id>\d+)')
    def product_add_to_cart(self, request, *args, **kwargs):
        cart = self.get_cart(self.request)
        product = get_object_or_404(Product, id=kwargs['product_id'])
        if self.request.user.is_authenticated:
            cart_product, created = self._get_or_create_cart_product(self.request.user.customer, cart, product, qty=self.request.data.get('qty'))
        else:
            cart_product, created = self._get_or_create_cart_product(None, cart, product, qty=self.request.data.get('qty'))
        if created:
            cart.products.add(cart_product)
            cart.save()
            if cart.payment_method.name == 'Wallet':
                cart.payment_method = Payment.objects.filter(name=request.data['payment']).first()
            # cart.wallet_payment = 0
            cart.save()
            return Response({"detail": "Товар добавлен в корзину", "added": True})
        if cart_product:
            cart_product.qty = self.request.data.get('qty')
            cart_product.save()
            cart.save()
            return Response({"detail": "Qty addeded", "added": True})
        return Response({'detail': "ERROR_ADD", "added": False}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["patch"], detail=False, url_path='current_customer_cart/change_qty/(?P<qty>\d+)/(?P<cart_product_id>\d+)')
    def product_change_qty(self, request, *args, **kwargs):
        cart_product = get_object_or_404(CartProduct, id=kwargs['cart_product_id'])
        cart_product.qty = int(kwargs['qty'])
        cart_product.save()
        cart_product.cart.save()
        if cart_product.cart.payment_method.name == 'Wallet':
            cart_product.cart.payment_method = Payment.objects.filter(name=request.data['payment']).first()
        # cart_product.cart.wallet_payment = 0
        cart_product.cart.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=["put"], detail=False, url_path='current_customer_cart/remove_from_cart/(?P<cproduct_id>\d+)')
    def product_remove_from_cart(self, request, *args, **kwargs):
        cart = self.get_cart(self.request)
        cproduct = get_object_or_404(CartProduct, id=kwargs['cproduct_id'])
        cart.products.remove(cproduct)
        cproduct.delete()
        cart.save()
        if cart.payment_method.name == 'Wallet':
            cart.payment_method = Payment.objects.filter(name=request.data['payment']).first()
        # cart.wallet_payment = 0
        cart.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["put"], detail=False, url_path='current_customer_cart/set_currency/(?P<currency_id>\d+)')
    def set_currency(self, *args, **kwargs):
        cart = self.get_cart(self.request)
        currency = get_object_or_404(Currency, id=kwargs['currency_id'])
        cart.currency = currency
        # for item in cart.products.all():
        #     item.currency = currency
        #     item.save()
        cart.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @logger.catch
    @action(methods=["put"], detail=False, url_path='current_customer_cart/set_payment')
    def set_payment(self, request, *args, **kwargs):
        payment = Payment.objects.filter(name=request.data.get('payment')).first()
        cart = self.get_cart(self.request)
        if payment.payoptions.count() > 0:
            cart.payoption = payment.payoptions.filter(id=request.data.get('payoption')).first()
        else:
            cart.payoption = None
        if cart.for_anonymous_user == True:
            cart.wallet_payment = 0
            if payment:
                cart.payment_method = payment
            cart.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        wallet = Wallet.objects.filter(owner=request.user.customer).first()
        try:
            if request.data.get('status') == 'true':
                cart.wallet_payment = wallet.balance
                cart.payment_method = payment
                cart.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            if request.data.get('status') == 'false':
                cart.wallet_payment = 0
                if payment:
                    cart.payment_method = payment
                cart.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as d:
            return Response({'detail': 'Exception'} ,status=status.HTTP_400_BAD_REQUEST)


