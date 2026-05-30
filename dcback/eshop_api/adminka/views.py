from dataclasses import fields
import decimal
from datetime import datetime, timedelta, date
import time
from operator import indexOf
from .utils.utils import construct, construct_selectors
import json
import django_filters
from django.core import serializers as SeriaLizer
from django_filters.rest_framework import DjangoFilterBackend
import jsons
from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import render
from eshop.models import Order, Polzov, Wallet, Customer, User, WalletOrder, Product, Brand, Limit, \
    PaymentCallback, Jsonfile, Cart, CartProduct, Category
from eshop.serializers import WalletSerializer, UsersSerializer, WalletOrdersSerializer, \
    CustomersSerializer
from apps.accounts.models import *
from eshop.Utilss.utils import json_read, json_save, get_or_create_token, create_token
from eshop_api.adminka.serializers import LimitsSerializer, pay_method_amounts, \
    wallet_balance, view_model, PaymentCallbackSerializer, WordersSerializer,CustomerSerializer, \
     BrandSerializer, ProductSerializer, CartsSerializer, CartProductSerializer, \
            WalletSerializer, Orders3Serializer, OrdersSerializer, OrdersSerializerLight, CategorySerializer
from eshop_api.main.serializers import ProductsSerializer, BrandsSerializer
from eshop_api.pagination import OrdersPagination, CustomerPagination, ProductsPagination
from eshop_api.utils import wallet_transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from loguru import logger
from django.db import transaction
from .utils.filters.q_objconst import *
from .utils.filters.grouping import *

def admin_index(request):
    return render(request, 'index.html', {})

class CategoriesViewSet(ModelViewSet):

    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CategorySerializer
    pagination_class = OrdersPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'id']


    def list(self, request, *args, **kwargs):
        
        logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
        Orders2ViewSet = logger.bind(name="Orders2ViewSet")
        
       
        if request.query_params.get('group'):
            if request.query_params.get('filter'):
                res2 = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
                self.queryset = self.queryset.filter(res2)
                   
            
            resdata = grup_constructor(request, json.loads(request.query_params.get('group')), self.queryset)                     
            return Response({'data': resdata[0], 'summary': resdata[1]}) 
                    
        if request.query_params.get('filter'):
            res = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
            self.queryset = self.queryset.filter(res)

        sort = ''
        if request.query_params.get('sort'):
            sort = json.loads(request.query_params.get('sort'))[0].get('selector').replace('.','__').replace('[0]','')
            if json.loads(request.query_params.get('sort'))[0].get('desc'):
                sort = f"-{sort}"
            self.queryset = self.queryset.order_by(sort)
                 
        response = super().list(request, *args, **kwargs)
        
        if request.query_params.get('totalSummary') and len(json.loads(request.query_params.get('totalSummary'))) > 0:
            qs = self.queryset
            try:
                response.data['summary'] = [getsumary(request, qs)]
            except:
                response.data = {'data': response.data, 'summary':getsumary(request, qs)}

        return response
    
    
    def update(self, request, *args, **kwargs):
        queryset = self.queryset.filter(pk=request.data.get('key'))
        queryset.update(**json.loads(request.data.get('values')))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

    def create(self, request, *args, **kwargs):
        # logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
        # Orders2ViewSet = logger.bind(name="Orders2ViewSet")
        data = json.loads(request.data.get('values'))
        # cat = data.pop('category')
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            obj = serializer.save()
            # obj.category.set(cat)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Orders2ViewSet(ModelViewSet):

    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = Orders3Serializer
    pagination_class = OrdersPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'id']
    # http_method_names = ['patch' ,'options','delete' ,'get' ,'post' ,'put'  ]
    
    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     # logger.add("logs/file_init.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "file_init")
    #     # file_init = logger.bind(name="file_init")
    #     # file_init.info(self.action)
    #     act = ['create', 'retrieve', 'update', 'destroy', 'partial_update']
    #     if self.action in act:
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]
    
    
    def list(self, request, *args, **kwargs):
        
        logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
        Orders2ViewSet = logger.bind(name="Orders2ViewSet")
        
       
        if request.query_params.get('group'):
            if request.query_params.get('filter'):
                res2 = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
                self.queryset = self.queryset.filter(res2)
                   
            
            resdata = grup_constructor(request, json.loads(request.query_params.get('group')), self.queryset)                     
            return Response({'data': resdata[0], 'summary': resdata[1]}) 
                    
        if request.query_params.get('filter'):
            res = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
            self.queryset = self.queryset.filter(res)

        sort = ''
        if request.query_params.get('sort'):
            sort = json.loads(request.query_params.get('sort'))[0].get('selector').replace('.','__').replace('[0]','')
            if json.loads(request.query_params.get('sort'))[0].get('desc'):
                sort = f"-{sort}"
            self.queryset = self.queryset.order_by(sort)
                 
        response = super().list(request, *args, **kwargs)
        
        if request.query_params.get('totalSummary') and len(json.loads(request.query_params.get('totalSummary'))) > 0:
            qs = self.queryset
            try:
                response.data['summary'] = [getsumary(request, qs)]
            except:
                response.data = {'data': response.data, 'summary':getsumary(request, qs)}

        return response
    
    
    def update(self, request, *args, **kwargs):
        queryset = self.queryset.filter(pk=request.data.get('key'))
        queryset.update(**json.loads(request.data.get('values')))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WordersViewSet(ModelViewSet):

    queryset = WalletOrder.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = WordersSerializer
    pagination_class = OrdersPagination
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['customer', 'id']
    # http_method_names = ['patch' ,'options','delete' ,'get' ,'post' ,'put'  ]
    
    
    def list(self, request, *args, **kwargs):
        logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
        Orders2ViewSet = logger.bind(name="Orders2ViewSet")
        
        
        if request.query_params.get('group'):
            if request.query_params.get('filter'):
                res2 = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
                self.queryset = self.queryset.filter(res2)
                   
            
            resdata = grup_constructor(request, json.loads(request.query_params.get('group')), self.queryset)                     
            return Response({'data': resdata[0], 'summary': resdata[1]}) 
                    
        if request.query_params.get('filter'):
            res = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
            self.queryset = self.queryset.filter(res)

        sort = ''
        if request.query_params.get('sort'):
            sort = json.loads(request.query_params.get('sort'))[0].get('selector').replace('.','__').replace('[0]','')
            if json.loads(request.query_params.get('sort'))[0].get('desc'):
                sort = f"-{sort}"
            self.queryset = self.queryset.order_by(sort)
                 
        response = super().list(request, *args, **kwargs)
        
        if request.query_params.get('totalSummary') and len(json.loads(request.query_params.get('totalSummary'))) > 0:
            qs = self.queryset
            try:
                response.data['summary'] = [getsumary(request, qs)]
            except:
                response.data = {'data': response.data, 'summary':getsumary(request, qs)}

        return response
    
    
    def update(self, request, *args, **kwargs):
        queryset = self.queryset.filter(pk=request.data.get('key'))
        queryset.update(**json.loads(request.data.get('values')))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
class CustomersViewSet(ModelViewSet):

    queryset = Customer.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CustomerSerializer
    pagination_class = CustomerPagination
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['user']
    # http_method_names = ['patch' ,'options','delete' ,'get' ,'post' ,'put'  ]
    
    
    def list(self, request, *args, **kwargs):
        logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
        Orders2ViewSet = logger.bind(name="Orders2ViewSet")
        
        
        if request.query_params.get('group'):
            if request.query_params.get('filter'):
                res2 = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
                self.queryset = self.queryset.filter(res2)
                   
            
            resdata = grup_constructor(request, json.loads(request.query_params.get('group')), self.queryset)                     
            return Response({'data': resdata[0], 'summary': resdata[1]}) 
                    
        if request.query_params.get('filter'):
            res = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
            self.queryset = self.queryset.filter(res)

        sort = ''
        if request.query_params.get('sort'):
            sort = json.loads(request.query_params.get('sort'))[0].get('selector').replace('.','__').replace('[0]','')
            if json.loads(request.query_params.get('sort'))[0].get('desc'):
                sort = f"-{sort}"
            self.queryset = self.queryset.order_by(sort)
                 
        response = super().list(request, *args, **kwargs)
        
        if request.query_params.get('totalSummary') and len(json.loads(request.query_params.get('totalSummary'))) > 0:
            qs = self.queryset
            try:
                response.data['summary'] = [getsumary(request, qs)]
            except:
                response.data = {'data': response.data, 'summary':getsumary(request, qs)}

        return response
    
    
    def update(self, request, *args, **kwargs):
        queryset = self.queryset.filter(pk=request.data.get('key'))
        queryset.update(**json.loads(request.data.get('values')))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
                
    
class LoginstatViewSet(ModelViewSet):

    # queryset = LoginStatistic.objects.all()
    permission_classes = [IsAdminUser]
    # serializer_class = LoginStatSerializer
    pagination_class = CustomerPagination
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['user']
    
    
    def list(self, request, *args, **kwargs):
        logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
        Orders2ViewSet = logger.bind(name="Orders2ViewSet")
        
        
        if request.query_params.get('group'):
            if request.query_params.get('filter'):
                res2 = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
                self.queryset = self.queryset.filter(res2)
                   
            
            resdata = grup_constructor(request, json.loads(request.query_params.get('group')), self.queryset)                     
            return Response({'data': resdata[0], 'summary': resdata[1]}) 
                    
        if request.query_params.get('filter'):
            res = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
            self.queryset = self.queryset.filter(res)

        sort = ''
        if request.query_params.get('sort'):
            sort = json.loads(request.query_params.get('sort'))[0].get('selector').replace('.','__').replace('[0]','')
            if json.loads(request.query_params.get('sort'))[0].get('desc'):
                sort = f"-{sort}"
            self.queryset = self.queryset.order_by(sort)
                 
        response = super().list(request, *args, **kwargs)
        
        if request.query_params.get('totalSummary') and len(json.loads(request.query_params.get('totalSummary'))) > 0:
            qs = self.queryset
            try:
                response.data['summary'] = [getsumary(request, qs)]
            except:
                response.data = {'data': response.data, 'summary':getsumary(request, qs)}

        return response
    
    
    def update(self, request, *args, **kwargs):
        queryset = self.queryset.filter(pk=request.data.get('key'))
        queryset.update(**json.loads(request.data.get('values')))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
       
    
class Brands2ViewSet(ModelViewSet):

    queryset = Brand.objects.all()
    # permission_classes = [IsAdminUser]
    serializer_class = BrandSerializer
    pagination_class = ProductsPagination
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['user']
    
    
    def list(self, request, *args, **kwargs):
        logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
        Orders2ViewSet = logger.bind(name="Orders2ViewSet")
        
        
        if request.query_params.get('group'):
            if request.query_params.get('filter'):
                res2 = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
                self.queryset = self.queryset.filter(res2)
                   
            
            resdata = grup_constructor(request, json.loads(request.query_params.get('group')), self.queryset)                     
            return Response({'data': resdata[0], 'summary': resdata[1]}) 
                    
        if request.query_params.get('filter'):
            res = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
            self.queryset = self.queryset.filter(res)

        sort = ''
        if request.query_params.get('sort'):
            sort = json.loads(request.query_params.get('sort'))[0].get('selector').replace('.','__').replace('[0]','')
            if json.loads(request.query_params.get('sort'))[0].get('desc'):
                sort = f"-{sort}"
            self.queryset = self.queryset.order_by(sort)
                 
        response = super().list(request, *args, **kwargs)
        
        if request.query_params.get('totalSummary') and len(json.loads(request.query_params.get('totalSummary'))) > 0:
            qs = self.queryset
            try:
                response.data['summary'] = [getsumary(request, qs)]
            except:
                response.data = {'data': response.data, 'summary':getsumary(request, qs)}

        return response
    
    
    def update(self, request, *args, **kwargs):
        queryset = self.queryset.filter(pk=request.data.get('key'))
        ddata = json.loads(request.data.get('values'))
        if ddata.get('category'):
            cat = ddata.pop('category')
            for c in cat:
                queryset.first().category.add(c)
        queryset.update(**ddata)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
        Orders2ViewSet = logger.bind(name="Orders2ViewSet")
        data = json.loads(request.data.get('values'))
        cat = data.pop('category')
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            obj = serializer.save()
            obj.category.set(cat)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # def create(self, request, *args, **kwargs):
    #     logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
    #     Orders2ViewSet = logger.bind(name="Orders2ViewSet")
    #     # queryset = self.queryset.filter(pk=request.data.get('key'))
    #     # queryset.update(**json.loads(request.data.get('values')))
    #     # serializer = self.get_serializer(queryset, many=True)
    #     # return Response(serializer.data)
    #     # Orders2ViewSet.info(f'request - {request.data.get("values")}')
    #     # Orders2ViewSet.info(f'args - {args}')
    #     # Orders2ViewSet.info(f'kwargs - {kwargs}')
    #     # d = request.data
    #     # request.data = json.loads(request.data.get("values"))
    #     # Orders2ViewSet.info(f'request.data.update - {kwargs}')
    #     return super().create(request, *args, **kwargs)


class Product2ViewSet(ModelViewSet):

    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    pagination_class = OrdersPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'title', 'brand']
    
    
    def list(self, request, *args, **kwargs):
        logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
        Orders2ViewSet = logger.bind(name="Orders2ViewSet")
        
        
        if request.query_params.get('group'):
            if request.query_params.get('filter'):
                res2 = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
                self.queryset = self.queryset.filter(res2)
                   
            
            resdata = grup_constructor(request, json.loads(request.query_params.get('group')), self.queryset)                     
            return Response({'data': resdata[0], 'summary': resdata[1]}) 
                    
        if request.query_params.get('filter'):
            res = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
            self.queryset = self.queryset.filter(res)

        sort = ''
        if request.query_params.get('sort'):
            sort = json.loads(request.query_params.get('sort'))[0].get('selector').replace('.','__').replace('[0]','')
            if json.loads(request.query_params.get('sort'))[0].get('desc'):
                sort = f"-{sort}"
            self.queryset = self.queryset.order_by(sort)
                 
        response = super().list(request, *args, **kwargs)
        
        if request.query_params.get('totalSummary') and len(json.loads(request.query_params.get('totalSummary'))) > 0:
            qs = self.queryset
            try:
                response.data['summary'] = [getsumary(request, qs)]
            except:
                response.data = {'data': response.data, 'summary':getsumary(request, qs)}

        return response
    
    
    def update(self, request, *args, **kwargs):
        queryset = self.queryset.filter(pk=request.data.get('key'))
        queryset.update(**json.loads(request.data.get('values')))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
             

class CartsViewSet(ModelViewSet):

    queryset = Cart.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CartsSerializer
    pagination_class = OrdersPagination
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['user']
    
    
    def list(self, request, *args, **kwargs):
        logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
        Orders2ViewSet = logger.bind(name="Orders2ViewSet")
        
        
        if request.query_params.get('group'):
            if request.query_params.get('filter'):
                res2 = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
                self.queryset = self.queryset.filter(res2)
                   
            
            resdata = grup_constructor(request, json.loads(request.query_params.get('group')), self.queryset)                     
            return Response({'data': resdata[0], 'summary': resdata[1]}) 
                    
        if request.query_params.get('filter'):
            res = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
            self.queryset = self.queryset.filter(res)

        sort = ''
        if request.query_params.get('sort'):
            sort = json.loads(request.query_params.get('sort'))[0].get('selector').replace('.','__').replace('[0]','')
            if json.loads(request.query_params.get('sort'))[0].get('desc'):
                sort = f"-{sort}"
            self.queryset = self.queryset.order_by(sort)
                 
        response = super().list(request, *args, **kwargs)
        
        if request.query_params.get('totalSummary') and len(json.loads(request.query_params.get('totalSummary'))) > 0:
            qs = self.queryset
            try:
                response.data['summary'] = [getsumary(request, qs)]
            except:
                response.data = {'data': response.data, 'summary':getsumary(request, qs)}

        return response
    
    
    def update(self, request, *args, **kwargs):
        queryset = self.queryset.filter(pk=request.data.get('key'))
        queryset.update(**json.loads(request.data.get('values')))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CartProductViewSet(ModelViewSet):

    queryset = CartProduct.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CartProductSerializer
    pagination_class = OrdersPagination
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['user']
    
    
    def list(self, request, *args, **kwargs):
        logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
        Orders2ViewSet = logger.bind(name="Orders2ViewSet")
        
        
        if request.query_params.get('group'):
            if request.query_params.get('filter'):
                res2 = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
                self.queryset = self.queryset.filter(res2)
                   
            
            resdata = grup_constructor(request, json.loads(request.query_params.get('group')), self.queryset)                     
            return Response({'data': resdata[0], 'summary': resdata[1]}) 
                    
        if request.query_params.get('filter'):
            res = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
            self.queryset = self.queryset.filter(res)

        sort = ''
        if request.query_params.get('sort'):
            sort = json.loads(request.query_params.get('sort'))[0].get('selector').replace('.','__').replace('[0]','')
            if json.loads(request.query_params.get('sort'))[0].get('desc'):
                sort = f"-{sort}"
            self.queryset = self.queryset.order_by(sort)
                 
        response = super().list(request, *args, **kwargs)
        
        if request.query_params.get('totalSummary') and len(json.loads(request.query_params.get('totalSummary'))) > 0:
            qs = self.queryset
            try:
                response.data['summary'] = [getsumary(request, qs)]
            except:
                response.data = {'data': response.data, 'summary':getsumary(request, qs)}

        return response
    
    
    def update(self, request, *args, **kwargs):
        queryset = self.queryset.filter(pk=request.data.get('key'))
        queryset.update(**json.loads(request.data.get('values')))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WalletViewSet(ModelViewSet):

    queryset = Wallet.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = WalletSerializer
    pagination_class = OrdersPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['owner', 'id']
    # http_method_names = ['patch' ,'options','delete' ,'get' ,'post' ,'put'  ]
        
    
    def list(self, request, *args, **kwargs):
        
        logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
        Orders2ViewSet = logger.bind(name="Orders2ViewSet")
        
       
        if request.query_params.get('group'):
            if request.query_params.get('filter'):
                res2 = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
                self.queryset = self.queryset.filter(res2)
                   
            
            resdata = grup_constructor(request, json.loads(request.query_params.get('group')), self.queryset)                     
            return Response({'data': resdata[0], 'summary': resdata[1]}) 
                    
        if request.query_params.get('filter'):
            res = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
            self.queryset = self.queryset.filter(res)

        sort = ''
        if request.query_params.get('sort'):
            sort = json.loads(request.query_params.get('sort'))[0].get('selector').replace('.','__').replace('[0]','')
            if json.loads(request.query_params.get('sort'))[0].get('desc'):
                sort = f"-{sort}"
            self.queryset = self.queryset.order_by(sort)
                 
        response = super().list(request, *args, **kwargs)
        
        if request.query_params.get('totalSummary') and len(json.loads(request.query_params.get('totalSummary'))) > 0:
            qs = self.queryset
            try:
                response.data['summary'] = [getsumary(request, qs)]
            except:
                response.data = {'data': response.data, 'summary':getsumary(request, qs)}

        return response
    
    
    def update(self, request, *args, **kwargs):
        queryset = self.queryset.filter(pk=request.data.get('key'))
        queryset.update(**json.loads(request.data.get('values')))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# class PfMutationsViewSet(ModelViewSet):

#     queryset = Pfmutations.objects.all()
#     # permission_classes = [IsAdminUser]
#     serializer_class = PfmutationsSerializer
#     pagination_class = OrdersPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['customer', 'id']
    # http_method_names = ['patch' ,'options','delete' ,'get' ,'post' ,'put'  ]
    
    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     # logger.add("logs/file_init.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "file_init")
    #     # file_init = logger.bind(name="file_init")
    #     # file_init.info(self.action)
    #     act = ['create', 'retrieve', 'update', 'destroy', 'partial_update']
    #     if self.action in act:
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]
    
    
    def list(self, request, *args, **kwargs):
        logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
        Orders2ViewSet = logger.bind(name="Orders2ViewSet")
        
        
        if request.query_params.get('group'):
            if request.query_params.get('filter'):
                res2 = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
                self.queryset = self.queryset.filter(res2)
                   
            
            resdata = grup_constructor(request, json.loads(request.query_params.get('group')), self.queryset)                     
            return Response({'data': resdata[0], 'summary': resdata[1]}) 
                    
        if request.query_params.get('filter'):
            res = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
            self.queryset = self.queryset.filter(res)

        sort = ''
        if request.query_params.get('sort'):
            sort = json.loads(request.query_params.get('sort'))[0].get('selector').replace('.','__').replace('[0]','')
            if json.loads(request.query_params.get('sort'))[0].get('desc'):
                sort = f"-{sort}"
            self.queryset = self.queryset.order_by(sort)
                 
        response = super().list(request, *args, **kwargs)
        
        if request.query_params.get('totalSummary') and len(json.loads(request.query_params.get('totalSummary'))) > 0:
            qs = self.queryset
            try:
                response.data['summary'] = [getsumary(request, qs)]
            except:
                response.data = {'data': response.data, 'summary':getsumary(request, qs)}

        return response
    
    
    def update(self, request, *args, **kwargs):
        self.queryset.filter(pk=request.data.get('key')).update(**json.loads(request.data.get('values')))
        
        return super().update(request, *args, **kwargs)
#------------------------------------------------------------------------------------


class OrdersViewSet(ModelViewSet):

    queryset = Order.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = OrdersSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Order.objects.all()
        if self.request.query_params and list(self.request.query_params.values()) != ['']:
            q_object = Q()
            for key in self.request.query_params:
                q_object.add(Q([key, self.request.query_params.get(key)]), Q.AND)

            queryset = queryset.filter(q_object)
        return queryset
    @action(methods=['put'], detail=False, url_path='update_status/(?P<pk>\d+)')
    def update_status(self, request, pk):
        qs = Order.objects.filter(id=pk).first()
        if qs:
            qs.status = request.data['status']
            qs.save()
            return HttpResponse(status=status.HTTP_205_RESET_CONTENT)

    @action(methods=['get'], detail=False, url_path='get_pf_balance')
    def get_pf_balance(self, request):
        return Response({'amount':0})

    @action(methods=['get'], detail=False, url_path='list')
    def orders_list(self, request):
        qs = Order.objects.all()
        serializer = OrdersSerializerLight(qs, many=True)
        serializer_data = serializer.data
        return Response(serializer_data)

    @action(methods=['post'], detail=False, url_path='refund')
    @transaction.atomic
    def refund(self, request):
        try:
            with transaction.atomic():
                order = Order.objects.filter(id=request.data['orderid']).first()
                owner = User.objects.filter(id=request.data['userid']).first()
                wtrans = Wallet.objects.filter(description__contains=request.data['orderid'])
                if not wtrans or wtrans.count() == 1 and wtrans.first().typ == 'debit' \
                    or (wtrans.count() == 1 and wtrans.first().description[12:] == '| Thank you!') \
                    or (wtrans.count() == 1 and wtrans.first().typ == 'credit' and wtrans.first().description[:9] == 'Remaining'):
                    tr = wallet_transaction(owner.customer, 'credit', decimal.Decimal(request.data['amount']),
                                            f'Refund for order #{request.data["orderid"]}')
                if tr:
                    order.status = 'refunded'
                    order.cart.refund_amount = decimal.Decimal(request.data['amount'])
                    order.save()
                    order.cart.save()
                    ser_data = SeriaLizer.serialize('json', [tr], indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, 
                                                    fields=["owner","typ","amount","description","balance"])
                    final_data = json.loads(ser_data)[0].get('fields')
                    final_data.update({'status': "OK", 'owner': tr.owner.user.username})
                    return Response(final_data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"result":'ERROR'})
        except Exception as exc:
            return Response({"result":f'ERROR {exc}'},status=status.HTTP_400_BAD_REQUEST)
        

class Wallet2ViewSet(ModelViewSet):

    queryset = Wallet.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = WalletSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Wallet.objects.all()
        if self.request.query_params and list(self.request.query_params.values()) != ['']:
            q_object = Q()
            for key in self.request.query_params:
                q_object.add(Q([key, self.request.query_params.get(key)]), Q.AND)
            queryset = queryset.filter(q_object)
        return queryset


class UsersViewSet(ModelViewSet):

    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = UsersSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = User.objects.all()
        if self.request.query_params and list(self.request.query_params.values()) != ['']:
            q_object = Q()
            for key in self.request.query_params:
                q_object.add(Q([key, self.request.query_params.get(key)]), Q.AND)
            queryset = queryset.filter(q_object)
        return queryset


class WalletOrdersView(ModelViewSet):

    queryset = WalletOrder.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = WalletOrdersSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = WalletOrder.objects.all()
        if self.request.query_params and list(self.request.query_params.values()) != ['']:
            q_object = Q()
            for key in self.request.query_params:
                q_object.add(Q([key, self.request.query_params.get(key)]), Q.AND)
            queryset = queryset.filter(q_object)
        return queryset

    @action(methods=['post'], detail=False, url_path='re_credit')
    @transaction.atomic
    def re_credit_to_wallet(self, request):
        worder = WalletOrder.objects.filter(id=request.data.get('id')).first()
        wtrans = Wallet.objects.filter(description__contains=worder.id)
        if worder and worder.status != 'completed' and not wtrans:
            tr = wallet_transaction(worder.owner, 'credit', round((worder.europrice / (worder.payment_method.fee_rate+100) * 100)\
                - worder.payment_method.fee_fix,2), f'Top-Up with {worder.payment_method.name} #{worder.id}')
            if tr:
                worder.status = 'completed'
                worder.save()
                ser_data = SeriaLizer.serialize('json', [tr], indent=2, use_natural_foreign_keys=True, use_natural_primary_keys=True, 
                                                fields=["owner", "amount", "typ", "description", "balance"])
                final_data = json.loads(ser_data)[0].get('fields')
                final_data.update({'status': "OK", 'owner': tr.owner.user.username})
                return Response(final_data, status=status.HTTP_201_CREATED)
            else:
                return Response({"status":"ERROR", "details": "WALLET TRANSACTION NOT CREATED"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status":"BAD REQUEST","details": "OPERATION NOT PERMITED - Invalid Order Status"}, status=status.HTTP_400_BAD_REQUEST)


class ProductsView(ModelViewSet):

    queryset = Product.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = ProductsSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Product.objects.all()
        if self.request.query_params and list(self.request.query_params.values()) != ['']:
            q_object = Q()
            for key in self.request.query_params:
                q_object.add(Q([key, self.request.query_params.get(key)]), Q.AND)
            queryset = queryset.filter(q_object)
        return queryset


class BrandsView(ModelViewSet):

    queryset = Brand.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = BrandsSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Brand.objects.all()
        if self.request.query_params and list(self.request.query_params.values()) != ['']:
            q_object = Q()
            for key in self.request.query_params:
                q_object.add(Q([key, self.request.query_params.get(key)]), Q.AND)
            queryset = queryset.filter(q_object)
        return queryset


class LimitsView(ModelViewSet):

    queryset = Limit.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = LimitsSerializer


# class LoginStatView(ModelViewSet):

#     queryset = LoginStatistic.objects.all()
#     permission_classes = [IsAdminUser]
#     serializer_class = LoginStatSerializer

#     def get_queryset(self):
#         """
#         Optionally restricts the returned purchases to a given user,
#         by filtering against a `username` query parameter in the URL.
#         """
#         queryset = LoginStatistic.objects.all()
#         if self.request.query_params and list(self.request.query_params.values()) != ['']:
#             q_object = Q()
#             for key in self.request.query_params:
#                 q_object.add(Q([key, self.request.query_params.get(key)]), Q.AND)
#             queryset = queryset.filter(q_object)
#         return queryset


class PaymentCallbackView(ModelViewSet):

    queryset = PaymentCallback.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = PaymentCallbackSerializer


class AdminAPI(ModelViewSet):
    logger.add("logs/admin-ui/adminAPI.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "adminAPI_log")
    adminAPI_log = logger.bind(name="adminAPI_log")
    # queryset = LoginStatistic.objects.filter(ip='kurva')
    permission_classes = [IsAdminUser]
    # serializer_class = LoginStatSerializer

    @action(methods=['POST'], detail=False, url_path='get')
    def get_data(self, request, *args, **kwargs):
        adminAPI_log = logger.bind(name="adminAPI_log")
        try:
            r = jsons.loads(request.body)
            if r.get('action') == 'dashboard':
                return Response(pay_method_amounts(r.get('date_from'), r.get('date_to')))
            if r.get('action') == 'balances':
                return Response(wallet_balance())
            if r.get('action') == 'user_wallet_balance':
                return Response(wallet_balance(r.get('user')))
            if r.get('action') == 'model':
                return Response(view_model(r.get('model')))
            if r.get('action') == 'SHOPSETTINGS':
                try:
                    data = Jsonfile.objects.filter(name='Shopsettings').first()
                    if data.json and r.get('data'):
                        # if data.json['updated_at'] <= r.get('data')['updated_at']:
                        data.json = r.get('data')
                        data.json['updated_at']=int(1000*datetime.now().timestamp())
                        data.save()
                    return Response(data.json)
                except Exception as d:
                    return Response({'detail': str(d)})
            if r.get('action') == 'get_or_create_token':
                return Response({'token': get_or_create_token(r.get('username'))})
            if r.get('action') == 'refresh_token':
                return Response({'token': create_token(request)})
            if r.get('action') == 'limits':
                try:
                    data = Jsonfile.objects.filter(name='Limits').first()
                    if data.json and r.get('data') and r.get('data')['updated_at']:
                        if data.json['updated_at'] <= r.get('data')['updated_at']:
                            data.json = r.get('data')
                            data.json['updated_at']=int(1000*datetime.now().timestamp())
                            data.save()
                    return Response(data.json)
                except Exception as d:
                    return Response({'detail': str(d)})
            return Response({'detail':'BAD REQUEST'})
        except Exception as d:
            adminAPI_log.exception(d)


class ActionSViewSet(ModelViewSet):
    
    # queryset = LoginStatistic.objects.all()
    permission_classes = [IsAdminUser]
    # serializer_class = LoginStatSerializer


    def list(self, request, *args, **kwargs):
        from eshop.PrepaidForge.Order import get_orders
        from eshop.soap_neosurf import soap_get_trx_detail
        from eshop.payop.functions import check_inv_status
        # from eshop.models import WalletOrder
        if self.request.query_params.get('action') == 'keys_check':
            order = Order.objects.filter(id=self.request.query_params.get('id')).first()
            pf = order.cart.products.filter(product__brand__wsaler='Prepaidforge').first()
            kinguin = order.cart.products.filter(product__brand__wsaler='Kinguin').first()
            pfres = []
            if pf:
                start = int(1000 * (order.created_at - timedelta(minutes=5)).timestamp())
                end = int(1000 * (order.created_at + timedelta(days=1)).timestamp())
                page = 1
                while True:
                    response = get_orders(start, end, page)
                    result = response.json()
                    if response.status_code != 200:
                        pfres.append(result)
                        break
                    for item in result.get('content'):
                        if int(item.get('customOrderReference')[:6]) == order.id:
                            pfres.append(item)
                    if result.get('pageCount') < 2:
                        break
                    page += 1
                    if page == result.get('pageCount'):
                        break
                    time.sleep(1)
            kinguinres = None
            if kinguin:
                from eshop.kinguin.order import check, get_keys
                chk = check(self.request.query_params.get('id'), extern=True)
                result = get_keys(chk.get('results')[0].get('orderId'))
                kinguinres = [chk.get('results')[0], result[0]]
            res = [pfres, result]

        elif self.request.query_params.get('action') == 'neocheck':
            res = soap_get_trx_detail(self.request.query_params.get('id'), 'no')
            res = [[res]]
            
        elif self.request.query_params.get('action') == 'payop':
            res = check_inv_status(self.request.query_params.get('id')).json()
            res = [[res.get('data')]]
           
        elif self.request.query_params.get('action') == 'ordermail':
            from eshop.order_email_send import orderemail
            orderemail(self.request.query_params.get('id'))
            res = {"detail":"OK"}
           
        else:
            return Response({'ERROR':'BAD REQUEST'})
        return Response(res)
        # return super().list(request, *args, **kwargs)


class PolzovViewSet(ModelViewSet):

    queryset = Polzov.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = Orders3Serializer
    pagination_class = OrdersPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user', 'user__id', 'fingeprint', 'token']
    # http_method_names = ['patch' ,'options','delete' ,'get' ,'post' ,'put'  ]
    
    # def get_permissions(self):
    #     """
    #     Instantiates and returns the list of permissions that this view requires.
    #     """
    #     # logger.add("logs/file_init.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "file_init")
    #     # file_init = logger.bind(name="file_init")
    #     # file_init.info(self.action)
    #     act = ['create', 'retrieve', 'update', 'destroy', 'partial_update']
    #     if self.action in act:
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]
    
    
    def list(self, request, *args, **kwargs):
        
        # logger.add("logs/Orders2ViewSet.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "Orders2ViewSet")
        # Orders2ViewSet = logger.bind(name="Orders2ViewSet")
        
       
        if request.query_params.get('group'):
            if request.query_params.get('filter'):
                res2 = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
                self.queryset = self.queryset.filter(res2)
                   
            
            resdata = grup_constructor(request, json.loads(request.query_params.get('group')), self.queryset)                     
            return Response({'data': resdata[0], 'summary': resdata[1]}) 
                    
        if request.query_params.get('filter'):
            res = q_objconstr(json.dumps(json.loads(request.query_params.get('filter'))))
            self.queryset = self.queryset.filter(res)

        sort = ''
        if request.query_params.get('sort'):
            sort = json.loads(request.query_params.get('sort'))[0].get('selector').replace('.','__').replace('[0]','')
            if json.loads(request.query_params.get('sort'))[0].get('desc'):
                sort = f"-{sort}"
            self.queryset = self.queryset.order_by(sort)
                 
        response = super().list(request, *args, **kwargs)
        
        if request.query_params.get('totalSummary') and len(json.loads(request.query_params.get('totalSummary'))) > 0:
            qs = self.queryset
            try:
                response.data['summary'] = [getsumary(request, qs)]
            except:
                response.data = {'data': response.data, 'summary':getsumary(request, qs)}

        return response
    
    
    def update(self, request, *args, **kwargs):
        queryset = self.queryset.filter(pk=request.data.get('key'))
        queryset.update(**json.loads(request.data.get('values')))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)