import decimal
import os
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from datetime import datetime, timedelta
import django
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.db.models import Q
from eshop.PrepaidForge.Order import pf_product_order
from eshop.models import Category, Product, Brand, Order, Cart, Payment, Currency, WalletOrder, \
    Wallet, Verification, Customer, Jsonfile
from eshop.order_email_send import orderemail
from eshop.serializers import RegisterSerializer
from eshop.Utilss.utils import json_read, json_save
from eshop_api.utils import get_cart_and_products_in_cart, neosurf_pay_send, \
    wallet_transaction, create_login_stat, Verify
from loguru import logger
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from .serializers import ProductSerializer, CustomCategorySerializer, BrandSerializer, PaymentSerializer, VerificationSerializer
from ..cart.serializers import OrderSerializer, CurrencySerializer
from ..pagination import CategoryBrandsPagination, BrandProductsPagination
from eshop.payop.neosurf import neosurf_payop_send
from eshop.payop.safetypay import safetypay_send
from eshop.payop.banktransfer import banktr_pay_send
from eshop.payop.default import defaultpay_send
from eshop.payop.advcash import advcash_payop_send
from eshop.Utilss.utils import parsedict, limitcheck
from eshop.crypto.merchant import create_order
# from aws.imagerecogn import detekt_faces, RekognitionImage
# from aws.textract_python_kv_parser import analyze_id
from eshop.kinguin.order import kinguin_product_order
import base64
import pickle
from eshop_api.pagination import OrdersPagination
from rest_framework.permissions import IsAdminUser
from django.db import IntegrityError, transaction
from config import loginx
import requests
from eshop.Utilss.PriceRabatt import RabattCeck
import json
# import socks
# ip='127.0.0.10' # change your proxy's ip
# port = 6000 # change your proxy's port
# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
# socket.socket = socks.socksocket


class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CustomCategorySerializer
    permission_classes = []
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Category.objects.filter(active=True)
        slug = self.request.query_params.get('slug')
        if slug is not None:
            queryset = queryset.filter(slug=slug)
        return queryset

    @action(methods=["get"], detail=True)
    def category_brands(self, request, *args, **kwargs):
        self.pagination_class = CategoryBrandsPagination
        brands = Brand.objects.filter(category=self.get_object(), active=True)
        # cart, products_in_cart = get_cart_and_products_in_cart(request)
        queryset = self.filter_queryset(brands)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BrandSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)



class BrandViewSet(ModelViewSet):

    queryset = Brand.objects.filter(active=True).exclude(deleted=True)
    serializer_class = BrandSerializer
    # permission_classes = []
    # authentication_classes = []
    # filter_backends = [DjangoFilterBackend]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['id','title']
    search_fields = ['title']

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Brand.objects.filter(active=True).exclude(deleted=True)
        slug = self.request.query_params.get('slug')
        if slug is not None:
            queryset = queryset.filter(slug=slug)
        return queryset

    @action(methods=["get"], detail=True)
    def brand_products(self, request, *args, **kwargs):
        self.pagination_class = BrandProductsPagination
        products = Product.objects.filter(brand=self.get_object(), active=True)
        # brand = self.get_object()
        # for prod in products:
        #     if brand.in_stock == False:
        #         prod['qty'] = 0
        #     if prod.in_stock == False:
        #         prod['qty'] = 0

        if request.user.is_authenticated:
            cart, products_in_cart = get_cart_and_products_in_cart(request)
        queryset = self.filter_queryset(products)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            for product in serializer.data:
                data = Jsonfile.objects.filter(name='Shopsettings').first().json
                if data.get('Other').get('all_no_stock') and product['brand']['wsaler'] == 'Prepaidforge':
                    product['qty'] = 0
                if not product['brand']['in_stock']:
                    product['qty'] = 0
                if not product['in_stock']:
                    product['qty'] = 0
            if request.user.is_authenticated:
                for product in serializer.data:
                    product['in_cart'] = True if product['id'] in products_in_cart else False
            return self.get_paginated_response(serializer.data)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id','title','value','brand','brand__slug','price','region']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if request.user.is_authenticated:
            cart, products_in_cart = get_cart_and_products_in_cart(request)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer_data = serializer.data
            for product in serializer.data:
                data = Jsonfile.objects.filter(name='Shopsettings').first().json
                if data.get('Other').get('all_no_stock') and product['brand']['wsaler'] == 'Prepaidforge':
                    product['qty'] = 0
                if not product['brand']['in_stock']:
                    product['qty'] = 0
                if not product['in_stock']:
                    product['qty'] = 0
            if request.user.is_authenticated:
                if cart:
                    for product in serializer_data:
                        product['in_cart'] = True if product['id'] in products_in_cart else False
            return self.get_paginated_response(serializer_data)

        serializer = self.get_serializer(queryset, many=True)
        serializer_data = serializer.data
        for product in serializer.data:
            data = Jsonfile.objects.filter(name='Shopsettings').first().json
            if data.get('Other').get('all_no_stock') and product['brand']['wsaler'] == 'Prepaidforge':
                product['qty'] = 0
            if not product['brand']['in_stock']:
                product['qty'] = 0
            if not product['in_stock']:
                product['qty'] = 0
        if request.user.is_authenticated:
            if cart:
                for product in serializer_data:
                    product['in_cart'] = True if product['id'] in products_in_cart else False
        return Response(serializer_data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if request.user.is_authenticated:
            cart, products_in_cart = get_cart_and_products_in_cart(request)
        serializer_data = serializer.data
        if request.user.is_authenticated:
            if cart:
                serializer_data['in_cart'] = False if instance.id not in products_in_cart else True
        return Response(serializer_data)


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        logger.add("logs/login.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "login")
        login = logger.bind(name="login")
        from djoser.views import TokenCreateView
        # TokenCreateView
        return Response({})


class CurrentUserView(APIView):

    def get(self, request, *args, **kwargs):
        ucontr = ''
        vers =  3569
        if request.user.is_authenticated:
            if not request.user.first_name or not request.user.last_name:
                ucontr = ['accdata']
            if request.user.is_superuser:
                return Response({'is_authenticated': True, 'is_admin': True, 'verst': vers})
            return Response({'is_authenticated': True, 'uc': ucontr, 'verst': vers})
        return Response({'is_authenticated': False, 'verst': vers})


class UserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        ucontr = ''
        vers =  3569
        if request.user.is_authenticated:
            if not request.user.first_name or not request.user.last_name:
                ucontr = ['accdata']
            if request.user.is_superuser:
                return Response({'is_authenticated': True, 'is_admin': True, 'verst': vers})
            return Response({'is_authenticated': True, 'uc': ucontr, 'verst': vers})
        return Response({'is_authenticated': False, 'verst': vers})
    
    
    def put(self, request, *args, **kwargs):
                    
        try:
            if request.user.is_authenticated:
                update = False
                if request.user.customer.status == 'Unverified' and request.user.customer.rolle == 'new':
                    update = True
                try:
                    if request.data and request.data.get('formdata').get('action') == 'update':
                        if request.data.get('formdata').get('first_name') or update == True:
                            if not request.user.first_name or update == True:
                                request.user.first_name = request.data.get('formdata').get('first_name')
                        if request.data.get('formdata').get('last_name') or update == True:
                            if not request.user.last_name or update == True:
                                request.user.last_name = request.data.get('formdata').get('last_name')
                        if request.data.get('formdata').get('phone') or update == True:
                            if not request.user.customer.phone or update == True:
                                request.user.customer.phone = request.data.get('formdata').get('phone')
                        if request.data.get('formdata').get('date_of_birth') or update == True:
                            if not request.user.customer.date_of_birth or update == True:
                                request.user.customer.date_of_birth = request.data.get('formdata').get('date_of_birth')
                        if request.data.get('formdata').get('street') or update == True:
                            if not request.user.customer.street or update == True:
                                request.user.customer.street = request.data.get('formdata').get('street')
                        # if request.data['formdata'].get('street2'):
                        #     if not request.user.customer.street2 or update == True:
                        #         request.user.customer.street2 = request.data['formdata'].get('street2')
                        if request.data.get('formdata').get('city') or update == True:
                            if not request.user.customer.city or update == True:
                                request.user.customer.city = request.data.get('formdata').get('city')
                        if request.data.get('formdata').get('postal_code') or update == True:
                            if not request.user.customer.postal_code or update == True:
                                request.user.customer.postal_code = request.data.get('formdata').get('postal_code')
                        if request.data.get('formdata').get('country_code'):
                            if not request.user.customer.country_code or update == True:
                                request.user.customer.country_code = request.data.get('formdata').get('country_code')
                        
                        request.user.save()
                        request.user.customer.save()
                except KeyError as d:
                    logger.exception('Keyerror')
                return Response({'username': request.user.username,
                                 'email': request.user.email,
                                 'first_name': request.user.first_name,
                                 'last_name': request.user.last_name,
                                 'date_of_birth': request.user.customer.date_of_birth,
                                 'phone': request.user.customer.phone,
                                 'street': request.user.customer.street,
                                 'city': request.user.customer.city,
                                 'postal_code': request.user.customer.postal_code,
                                 'country_code': request.user.customer.country_code,
                                 'status': request.user.customer.status,
                                 })
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as d:
            logger.exception('last')
            return Response({'detail':f'{str(d)} {request.user.customer.status}'})



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class OrderViewSet(ModelViewSet):
    logger.add("logs/order.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "order_log")
    order_log = logger.bind(name="order_log")
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    pagination_class = OrdersPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['id']
    search_fields = ['id']

    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(customer=request.user.customer, deleted=False)
        response = super().list(request, *args, **kwargs)
        return response


    def update(self, request, *args, **kwargs):
        # return Response(request.data)
        order = self.queryset.filter(id=request.data.get('id')).first()
        request.data.get('json')['txid'] = list(set(request.data.get('json').get('txid')))
        order.json.update(request.data.get('json'))
        order.save()
        return Response(status=status.HTTP_201_CREATED)


    @logger.catch
    @action(methods=['post'], detail=False)
    def create_order(self, request):
        order_log = logger.bind(name="order_log")
        try:
            if Jsonfile.objects.filter(name='Shopsettings').first().json.get('Other').get('all_no_stock'):
                return Response({'message': 'SORRY PRODUCT TEMPORARILY OUT OF STOCK.'})
            
            cart = Cart.objects.get(owner=request.user.customer, in_order=False)
            if cart.payment_method.name != 'Cryptocurrency':  
                limitres = limitcheck(request)
                
                if limitres:
                    return Response({'detail': limitres+'_limit', 'message': limitres.capitalize()+' limit exceeded. '
                                                            'Please reduce the shopping cart or try again later.', 'v':request.user.customer.status})
            try:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            except:
                ip = request.META['REMOTE_ADDR']

            create = Order.objects.create(
                customer=request.user.customer,
                cart=cart,
                del_email=request.data['del_email'],
                ip=ip,
                json=request.data
                )
            if create:
                cart.owner.orders.add(create)
                cart.in_order = True
                cart.order = create
                cart.save()
                create.save()
                create.json.update({'curprice':str(create.pay_currency.price)})
                create.save()
                try:
                    create_login_stat(username=request.user.username,
                                    ip=ip,
                                    result=create.id, useragent=request.META.get('HTTP_USER_AGENT'),
                                    device=request.META.get('HTTP_SEC_CH_UA_PLATFORM'),
                                    meta=request.META)
                except:
                    pass
                return Response({"detail": "OK", 'id': create.id})
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        except Exception as d:
            order_log.exception(d)

    @logger.catch
    @action(methods=["post"], detail=False)
    def set_payment(self, request):
        cart = Cart.objects.get(owner=request.user.customer, in_order=False)
        # print()
        payment = Payment.objects.get(name=request.data['payment'])
        # cproduct = get_object_or_404(CartProduct, id=kwargs['cproduct_id'])
        cart.payment_method = payment
        cart.save()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    @logger.catch
    @action(methods=["post"], detail=False)
    def get_payment(self, request):
        order_log = logger.bind(name="order_log")
        if Jsonfile.objects.filter(name='Shopsettings').first().json.get('Other').get('TestModus') == False:
            test = 'no'
        else:
            test = 'yes'
        invoic = WalletOrder.objects.filter(status='completed').first().invoice
        order = Order.objects.filter(id=request.data['orderid']).first()
        worder = WalletOrder.objects.filter(id=request.data['orderid']).first()
        if order and order.status == 'pending_payment':
            if order.cart.payment_method.name == 'Wallet':
                wallet = Wallet.objects.filter(owner=request.user.customer).first()
                if wallet:
                    if order.cart.final_price > wallet.balance:
                        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
                    tr = wallet_transaction(order.customer, 'debit', -order.cart.final_price,
                                            f'Payment for order #{order.id}')
                    if tr:
                        order.status = 'processing'
                        order.save()
                        order.cart.save()
                        pf_roducts = order.cart.products.filter(product__brand__wsaler='Prepaidforge')
                        kinguin_products = order.cart.products.filter(product__brand__wsaler='Kinguin')
                        list_res = []
                        if pf_roducts:
                             pfres = pf_product_order(order, pf_roducts)
                             list_res.append(pfres)
                        if kinguin_products:
                            kinres = kinguin_product_order(order, kinguin_products)
                            list_res.append(kinres)
                        for r in list_res:
                            if r == 'ok':
                                final_res = 'ok'
                            else:
                                final_res = 'error'
                                break
                        if final_res == 'ok':
                            rch = RabattCeck(order)
                            rch.walletcredit()
                            order.status = 'completed'
                            order.save()
                        orderemail(order.id)
                        order.save()
                        order.cart.save()
                        return Response({"detail": "OK", "url": f'/myaccount/?myorders'})
                    else:
                        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
                else:
                    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
            # order_log.debug(f"4_")

            if order.cart.payment_method.name == 'Neosurf':
                # order_log = logger.bind(name="order_log")
                try:
                    amount = order.pay_amount
                    orderid = order.id
                    if amount > 0:
                    # if order.cart.currency.shortname == 'CAD':
                        result = neosurf_pay_send(orderqs=order, id=orderid, amount=amount, currency=order.cart.currency.shortname.lower(),
                                                test=test,
                                        urlOk=request.data['location'] + "/payments/" + str(orderid),
                                        urlKo=request.data['location'] + f"/cancel/{orderid}",
                                        urlPending=request.data['location'],
                                        urlCallback=request.data['location'] + "/callbck/" + str(orderid) + '/')
                        if result.get('detail') == "OK":
                            order.responsedata = result.get('url')
                            order.cart.save()
                            order.save()
                        else:
                            order.responsedata = result
                            order.status = 'cancelled'
                            order.deleted = True
                            order.cart.in_order = False
                            order.cart.order = None
                            order.cart.save()
                            order.save()
                        return Response(result)
                    
                    else:
                        result = neosurf_payop_send(type='o', orderqs=order, id=orderid, amount=amount, currency=order.cart.currency.shortname, 
                        test='no', urlOk=request.data['location'] + "/payments/" + str(orderid), urlKo=request.data['location'] + f"/cancel/{orderid}", 
                        email=order.customer.user.email, name=order.customer.user.first_name+' '+order.customer.user.last_name, ip=order.ip)
                        if result.get('detail') == "OK":
                            order.responsedata = result.get('url')
                            order.cart.save()
                            order.save()
                        else:
                            order.responsedata = result
                            order.status = 'cancelled'
                            order.deleted = True
                            order.cart.in_order = False
                            order.cart.order = None
                            order.cart.save()
                            order.save()
                        return Response(result)
                except Exception as d:
                    order_log.exception(d)

                    
            order_log = logger.bind(name="order_log")
            if order.cart.payment_method.name == 'Binance Pay':
                order_log.info(order.cart.payment_method.name)
                amount = order.pay_amount
                result = create_order(type='o', orderqs=order, amount=amount, currency="USDT", urlOk=request.data['location'] + "/payments/" + str(order.id), 
                            urlKo=request.data['location'] + "/payments/" + str(order.id), hookUrl=(request.data['location'] + "/binancewh").replace('www.',''))
                if result.get('status') == 'SUCCESS':
                    order.responsedata = result.get('data').get('universalUrl')
                    order.cart.save()
                    order.save()
                    return Response({"detail": "OK", "url":result.get('data').get('universalUrl')})
                else:
                    order.responsedata = result
                    order.status = 'cancelled'
                    order.cart.save()
                    order.save()
                    return Response({"detail": "error", "message":result.get('errorMessage')})

            if order.cart.payment_method.name == 'Cryptocurrency':
                order.responsedata = request.data['location'] + f"/payment/{order.id}"
                order.cart.save()
                order.save()
                return Response({"detail": "OK", "url": f"/payment/{order.id}"})
            
            if order.cart.payment_method.name == 'SafetyPay':
                result = safetypay_send(type='o', orderqs=order, id=order.id, amount=order.pay_amount, currency=order.cart.currency.shortname, 
                urlOk=request.data['location'] + "/payments/" + str(order.id), urlKo=request.data['location'] + f"/cancel/{order.id}", 
                email=order.customer.user.email, name=order.customer.user.first_name+' '+order.customer.user.last_name, ip=order.ip)
                if result.get('detail') == "OK":
                    order.responsedata = result.get('url')
                    order.cart.save()
                    order.save()
                else:
                    order.responsedata = result
                    order.status = 'cancelled'
                    order.deleted = True
                    order.cart.in_order = False
                    order.cart.order = None
                    order.cart.save()
                    order.save()
                return Response(result)
            

            if order.cart.payment_method.name == 'Advanced Cash':
                result = advcash_payop_send(type='o', orderqs=order, id=order.id, amount=order.pay_amount, currency=order.cart.currency.shortname, 
                urlOk=request.data['location'] + "/payments/" + str(order.id), urlKo=request.data['location'] + f"/cancel/{order.id}", 
                email=order.customer.user.email, name=order.customer.user.first_name+' '+order.customer.user.last_name, ip=order.ip)
                if result.get('detail') == "OK":
                    order.responsedata = result.get('url')
                    order.cart.save()
                    order.save()
                else:
                    order.responsedata = result
                    order.status = 'cancelled'
                    order.deleted = True
                    order.cart.in_order = False
                    order.cart.order = None
                    order.cart.save()
                    order.save()
                return Response(result)

            
            if order.cart.payment_method.desc == 'default':
                result = defaultpay_send(type='o', orderqs=order, id=order.id, amount=order.pay_amount, currency=order.cart.currency.shortname, 
                urlOk=request.data['location'] + "/payments/" + str(order.id), urlKo=request.data['location'] + f"/cancel/{order.id}", 
                email=order.customer.user.email, name=order.customer.user.first_name+' '+order.customer.user.last_name, ip=order.ip)
                if result.get('detail') == "OK":
                    order.responsedata = result.get('url')
                    order.cart.save()
                    order.save()
                else:
                    order.responsedata = result
                    order.status = 'cancelled'
                    order.deleted = True
                    order.cart.in_order = False
                    order.cart.order = None
                    order.cart.save()
                    order.save()
                return Response(result)

            
            if order.cart.payment_method.name == 'BankTransfer':
                result = banktr_pay_send(type='o', orderqs=order, id=order.id, amount=order.pay_amount, currency=order.cart.currency.shortname, 
                urlOk=request.data['location'] + "/payments/" + str(order.id), urlKo=request.data['location'] + f"/cancel/{order.id}", 
                email=order.customer.user.email, name=order.customer.user.first_name+' '+order.customer.user.last_name, 
                date_of_birth=order.customer.date_of_birth, ip=order.ip, payoption=order.cart.payoption.type)
                if result.get('detail') == "OK":
                    order.responsedata = result.get('url')
                    order.cart.save()
                    order.save()
                else:
                    order.responsedata = result
                    order.status = 'cancelled'
                    order.deleted = True
                    order.cart.in_order = False
                    order.cart.order = None
                    order.cart.save()
                    order.save()
                return Response(result)
       
        if worder and worder.status == 'pending_payment':
            if worder.payment_method.name == 'Neosurf':
                if worder.currency.shortname == 'CAD' or worder.total_price <=15 or invoic != None:
                    result = neosurf_pay_send(orderqs=worder, id=worder.id, amount=worder.total_price,
                                            currency=worder.currency.shortname.lower(), test=test,
                                    urlOk=request.data['location'] + "/payments/" + str(worder.id),
                                    urlKo=request.data['location'] + f"/cancel/{worder.id}",
                                    urlPending=request.data['location'],
                                    urlCallback=request.data['location'] + "/callbck/" + str(worder.id) + '/')
                    if result.get('detail') == "OK":
                        worder.responsedata = result.get('url')
                        worder.save()
                    else:
                        worder.responsedata = result
                        worder.save()
                    return Response(result)
               
                else:
                    result = neosurf_payop_send(type='w', orderqs=worder, id=str(worder.id), amount=str(worder.total_price), currency=worder.currency.shortname, 
                    test='no', urlOk=request.data['location'] + "/payments/" + str(worder.id), urlKo=request.data['location'] + f"/cancel/{worder.id}", 
                    email=worder.owner.user.email, name=worder.owner.user.first_name+' '+worder.owner.user.last_name, ip=worder.ip)
                    if result.get('detail') == "OK":
                        worder.responsedata = result.get('url')
                        worder.save()
                    else:
                        worder.responsedata = result
                        worder.save()
                    return Response(result)
            
            if worder.payment_method.name == 'Binance Pay':
                amount = worder.total_price
                result = create_order(type='w', orderqs=worder, amount=amount, currency="USDT", urlOk=request.data['location'] + "/payments/" + str(worder.id), 
                             urlKo=request.data['location'] + "/payments/" + str(worder.id), hookUrl=(request.data['location'] + "/binancewh").replace('www.',''))
                if result.get('status') == 'SUCCESS':
                    worder.responsedata = result.get('data').get('universalUrl')
                    worder.save()
                    return Response({"detail": "OK", "url":result.get('data').get('universalUrl')})
                else:
                    worder.responsedata = result
                    worder.status = 'cancelled'
                    worder.save()
                    return Response({"detail": "error", "message":result.get('errorMessage')})
                


            if worder.payment_method.name == 'Cryptocurrency':

                while True:
                    qs = Order.objects.filter(pay_currency=worder.currency, pay_amount=worder.total_price,
                                              status='pending_payment')
                    wqs = WalletOrder.objects.filter(currency=worder.currency, total_price=worder.total_price,
                                              status='pending_payment').exclude(id=worder.id)
                    if qs or wqs:
                        check = False
                        if qs:
                            for ord in qs:
                                if ord.pay_amount == worder.total_price:
                                    check = True
                        if wqs:
                            for word in wqs:
                                if word.total_price == worder.total_price:
                                    check = True
                        if check == True:
                            if worder.currency.shortname == 'USDT':
                                tofix = 2
                                add = 0.01
                            else:
                                add = 0.00000001
                                tofix = 8
                            worder.price += round(decimal.Decimal(add),tofix)
                            worder.save()
                        else:
                            break
                    else:
                        break
                worder.responsedata = request.data['location'] + f"/payment/{worder.id}"
                worder.save()
                return Response({"detail": "OK", "url": f"/payment/{worder.id}"})
        
            if worder.payment_method.name == 'SafetyPay':
                result = safetypay_send(type='w', orderqs=worder, id=str(worder.id), amount=str(worder.total_price), currency=worder.currency.shortname, 
                urlOk=request.data['location'] + "/payments/" + str(worder.id), urlKo=request.data['location'] + f"/cancel/{worder.id}", 
                email=worder.owner.user.email, name=worder.owner.user.first_name+' '+worder.owner.user.last_name, ip=worder.ip)
                if result.get('detail') == "OK":
                    worder.responsedata = result.get('url')
                    worder.save()
                else:
                    worder.responsedata = result
                    worder.save()
                return Response(result)
            

            if worder.payment_method.name == 'Advanced Cash':
                result = advcash_payop_send(type='w', orderqs=worder, id=str(worder.id), amount=str(worder.total_price), currency=worder.currency.shortname, 
                urlOk=request.data['location'] + "/payments/" + str(worder.id), urlKo=request.data['location'] + f"/cancel/{worder.id}", 
                email=worder.owner.user.email, name=worder.owner.user.first_name+' '+worder.owner.user.last_name, ip=worder.ip)
                if result.get('detail') == "OK":
                    worder.responsedata = result.get('url')
                    worder.save()
                else:
                    worder.responsedata = result
                    worder.save()
                return Response(result)
            

            if worder.payment_method.desc == 'default':
                result = defaultpay_send(type='w', orderqs=worder, id=str(worder.id), amount=str(worder.total_price), currency=worder.currency.shortname, 
                urlOk=request.data['location'] + "/payments/" + str(worder.id), urlKo=request.data['location'] + f"/cancel/{worder.id}", 
                email=worder.owner.user.email, name=worder.owner.user.first_name+' '+worder.owner.user.last_name, ip=worder.ip)
                if result.get('detail') == "OK":
                    worder.responsedata = result.get('url')
                    worder.save()
                else:
                    worder.responsedata = result
                    worder.save()
                return Response(result)

            
            if worder.payment_method.name == 'BankTransfer':
                result = banktr_pay_send(type='w', orderqs=worder, id=str(worder.id), amount=str(worder.total_price), currency=worder.currency.shortname, 
                urlOk=request.data['location'] + "/payments/" + str(worder.id), urlKo=request.data['location'] + f"/cancel/{worder.id}", 
                email=worder.owner.user.email, name=worder.owner.user.first_name+' '+worder.owner.user.last_name, 
                date_of_birth=worder.owner.date_of_birth, ip=worder.ip, payoption=worder.payoption.type)
                if result.get('detail') == "OK":
                    worder.responsedata = result.get('url')
                    worder.save()
                else:
                    worder.responsedata = result
                    worder.save()
                return Response(result)
        return Response({'message':'GENERAL ERROR'})




class PaymentView(ModelViewSet):
    queryset = Payment.objects.filter(enabled=True)
    permission_classes = [AllowAny]
    serializer_class = PaymentSerializer
    # pagination_class = CategoryBrandsPagination
    def list(self, request, *args, **kwargs):
        logger.add("logs/payment_view.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "payment_view")
        payment_view = logger.bind(name="payment_view")
        if request.user.is_authenticated:
            exclude = ['frmed114@gmail.com']
            payment_view.info(request.user.email)
            if request.user.email in exclude:
                self.queryset = self.queryset.exclude(name='Flexepin')
        response = super().list(request, *args, **kwargs)
        return response


class CurrencyView(ModelViewSet):
    queryset = Currency.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CurrencySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['id','shortname']
    search_fields = ['shortname']

    def list(self, request, *args, **kwargs):
        from eshop.crypto.bncecryptopayment.cryptopayment import CryptoPayment
        cp = CryptoPayment
        
        if request.query_params.get('assets') == '1':
            res = cp.getresponse(cp)
            return Response(res)

        # self.queryset = self.queryset.filter(customer=request.user.customer, deleted=False)
        response = super().list(request, *args, **kwargs)
        return response


class VerifView(APIView):

    # logger.add("verifi.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "verifi")
    # verifi = logger.bind(name="verifi")
    # logger.add("fileuload.log", backtrace=True, diagnose=True)
    # queryset = Verification.objects.all()
    # permission_classes = [IsAuthenticated]
    # http_method_names = ['get', 'post', 'patch', 'put', 'head', 'delete']
    permission_classes = [AllowAny]
    # serializer_class = VerificationSerializer
    # http_method_names = ['get']

    # @action(methods=['post'], detail=False)
    def get(self, request):
        verifi = logger.bind(name="verifi")
        if request.user.is_staff:
            qs = Verification.objects.all()
            serializer = VerificationSerializer(qs, many=True)
            return Response(serializer.data)
        else:
            return Response({})


    def post(self, request):
        verifi = logger.bind(name="verifi")
        import base64
        from base64 import b64encode, b64decode
        
        vqs = Verification.objects.filter(customer=request.user.customer).filter(status=None).last()
        if vqs:
            verif = Verify.get_verifications(vqs.verification_id, test=False).json()
            if verif and verif.get('status') and verif.get('status') == 'unused':
                request.user.customer.status = 'Under Review'
                request.user.customer.save()
                return vqs.form_url
                # return Response ({'form_url': vqs.form_url})
        
        res = Verify.start(request, test=False).json()
        if res and res.get('form_url'):
            create = Verification.objects.create(
                customer=request.user.customer,
                form_id=res.get('form_id'),
                form_url = res.get('form_url'),
                verification_id=res.get('verification_id'),
            )
            if create:
                request.user.customer.status = 'Under Review'
                request.user.customer.save()
                return res.get('form_url')
                # return Response ({'form_url': res.get('form_url')}, status=status.HTTP_200_OK)
            else:
                return 'There has been an error. Please try again.'
                # return Response({'detail':'There has been an error. Please try again.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return 'There has been an error. Please try again.'
            # return Response({'detail':'There has been an error. Please try again.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
                
    @transaction.atomic
    def put(self, request):
        verifi = logger.bind(name="verifi")
        # verifi.info(f'request.data: {request.data}')
        if request.user.is_staff:
            if request.data.get('delete'):
                qs = Verification.objects.filter(id=request.data.get('delete'))
                qs.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            
            try:
                with transaction.atomic():
                    vobj = Verification.objects.filter(id=request.data.get('id')).first()
                    v = request.data
                    for key, value in v.items():
                            setattr(vobj, key, value)
                    vobj.save()
                    cobj = Customer.objects.filter(user__id=vobj.customer.user.id).first()
                    if vobj.status == 'Aproved':
                        cobj.status = 'Verified'
                        cobj.save()
                    elif vobj.status == 'Under Review':
                        cobj.status = 'Under Review'
                        cobj.save()
                    else:
                        cobj.status = 'Unverified'
                        cobj.save()
                    return Response(status=status.HTTP_201_CREATED)
            except:
                verifi.exception('excepc')
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    # def delete(self, request, pk):
    #     if request.user.is_staff:
    #         verifi = logger.bind(name="verifi")
    #         verifi.info(f'request.data: {request.data}')
    #         verifi.info(f'pk: {pk}')
    #         return Response(pk)


class OtherView(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request):
        
        def check_blacklist(request):
            from eshop.models import Jsonfile
            jsf = Jsonfile.objects.filter(name='bnce_gc').first()
            lst =[]
            cart = request.COOKIES.get('_ccc')
            if cart in jsf.json.keys():
                lst.append(cart)
            ip = request.META.get('HTTP_X_REAL_IP')
            if ip in jsf.json.keys():
                lst.append(cart)
            userid = request.user.id
            if userid in jsf.json.keys():
                lst.append(cart)
            
            if len(lst) > 0:
                return (60*60*60 - (datetime.now().timestamp() - min(lst))) /60/60
            return None
        
        from eshop.crypto.bgiftcard import verify
        
        logger.add("logs/bnce_gc.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "bnce_gc_log")
        bnce_gc_log = logger.bind(name="bnce_gc_log")
        if request.data.get('bnce_gc_verify'):
            # return Response({'status':'error','msg':f'The gift card check is blocked for {"chck"} minutes due to a failed attempt.'})
            chck = check_blacklist(request)
            if chck:
                return Response({'status':'error','msg':f'The gift card check is blocked for {chck} minutes due to a failed attempt.'})
            result = verify(request=request, logger=bnce_gc_log)
            if result.get('status') != 'ok':
                return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            elif result.get('status') == 'ok':
                return Response(result, status=status.HTTP_200_OK)
            bnce_gc_log.error('no options_1')
            return Response({'status':'error','msg':'There has been an error. Please try again or contact support'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        if request.data.get('bnce_gc_redeem'):
            chck = check_blacklist(request)
            if chck:
                return Response({'status':'error','msg':f'The gift card check is blocked for {chck} minutes due to a failed attempt.'})

        bnce_gc_log.error('no options_2')
        return Response({'status':'error','msg':'There has been an error. Please try again or contact support'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        

    # def get(self, request):
    #     logger.add("logs/bnce_gc.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "bnce_gc_log")
    #     bnce_gc_log = logger.bind(name="bnce_gc_log")
    #     bnce_gc_log.info(request.COOKIES)
    #     response = Response({'header':request.data})
    #     response.set_cookie('_crt', 'dfgdfgdfgd645645645', httponly=True)
    #     return response