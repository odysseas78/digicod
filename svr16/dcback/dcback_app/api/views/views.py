import base64
from os import environ
from pprint import pprint
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.core import serializers as SeriaLizer
from loguru import logger
from rest_framework.views import APIView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, viewsets
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.db.models import Q, Avg, Count, Min, Sum, F
from api.serializers import SZ
from eshop.models import WalletOrder
from eshop.Utilss.utils import save_obj, read_obj
from eshop.order_email_send import orderemail
from eshop.serializers import WalletOrderSerializer
import itertools
import base64
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.renderers import JSONRenderer
from config.pagination import CustomPagination
from decimal import Decimal
from time import sleep
from api.utils.regionsfn import regionsfn
import pickle
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.views.decorators.csrf import ensure_csrf_cookie
ensure_csrf = method_decorator(ensure_csrf_cookie)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # oder str(obj) für eine Zeichenkettenrepräsentation
        # Lassen Sie die Basisklasse den Typenfehler werfen, falls nicht abgefangen
        return super(DecimalEncoder, self).default(obj)

def logfn1(name,path='logs/'):
    logger.add(f"{path}/{name}.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == name)
    return logger.bind(name=name)

def xor_cypher(input_string, key):
    encrypted = ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(input_string, itertools.cycle(key)))
    return encrypted



def encrypt(input_string, key='mysecretkey'):
    encrypted = xor_cypher(input_string, key)
    return base64.b64encode(encrypted.encode()).decode()

def decrypt(encrypted_string, key='mysecretkey'):
    encrypted = base64.b64decode(encrypted_string.encode()).decode()
    return xor_cypher(encrypted, key)




class ApiView(GenericAPIView):
  
    permission_classes = []
    pagination_class = CustomPagination
    ddd = 0
    # @ensure_csrf_cookie
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        # logger.add("logs/file_init.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "file_init")
        # file_init = logger.bind(name="file_init")
        # file_init.info(self.action)
        # rdata = {self.request.GET.get('u'):json.loads(self.request.GET.get('p')), 'request':self.request}
        act = ['GetUser','GetCustomer','GetWallet','GetOrder','GetWorder','GetSonst', 'GetCoinWallet','OrderSend','GetCoinWalletDeposit', 'GetCoinWalletTransaction']
        if self.request.GET.get('u') in act:
            permission_classes = [IsAuthenticated]
            self.ddd = 1
        else:
            permission_classes = [AllowAny]
            self.ddd = 2
        return [permission() for permission in permission_classes]

    # def get(self, request):
    #     rdata = {decrypt(request.GET.get('u')):json.loads(decrypt(request.GET.get('p'))), 'request':request}
    #     # logfn1('loginRegister').info(rdata)
    #     if self.ddd == 2:
    #         data=encrypt(json.dumps(json.loads(eval(f'GD.{list(rdata.keys())[0]}')(GD, rdata))))
    #         # logfn1('loginRegister').info(data)
    #         return Response(data, status=status.HTTP_200_OK)
    #     elif self.ddd == 1:
    #         data=encrypt(json.dumps(json.loads(eval(f'GDAuth.{list(rdata.keys())[0]}')(GDAuth, rdata))))
    #         return Response(data, status=status.HTTP_200_OK)
    # @ensure_csrf
    def get(self, request):
        # try:
        #     logfn1('getEncrypted').info(json.loads(decrypt(request.GET.get('p'))))
        #     rdata = {decrypt(request.GET.get('u')):json.loads(decrypt(request.GET.get('p'))), 'request':request}
        # except Exception as e:
        # rdata = {request.GET.get('u'):json.loads(request.GET.get('p')), 'request':request}
        rdata = {request.GET.get('u'):json.loads(request.GET.get('p')), 'request':request}

        # if request.GET.get('u') in ['GetCategory', 'GetBasket', 'GetCurrency', 'GetPayment']:
        # if request.GET.get('u') == 'GetBasket':
        #     logfn1('GetCategory','api/views/logs/').debug(f'{rdata} | {request.META.get("HTTP_X_REQUEST_ID")}')
            # logfn1('GetCategory','api/views/logs/').debug(f'{rdata} | {request.headers.get("X-Request-Id")}')
        # logfn1('ApiView','api/views/logs/').debug(f'{rdata} | {request.META.get("HTTP_AUTHORIZATION")}')
        if self.ddd == 2:
            # data=encrypt(json.dumps(json.loads(eval(f'GD.{list(rdata.keys())[0]}')(GD, rdata)))) if list(rdata.keys())[0] == 'GetBasket' else \
            #     json.loads(eval(f'GD.{list(rdata.keys())[0]}')(GD, rdata))
            # data = json.loads(eval(f'GD.{list(rdata.keys())[0]}')(GD, rdata))
            method_name = list(rdata.keys())[0]
            method = getattr(GD, method_name)
            data = json.loads(method(GD, rdata))
            return Response(data, status=status.HTTP_200_OK)
        elif self.ddd == 1:
            # data=json.loads(eval(f'GDAuth.{list(rdata.keys())[0]}')(GDAuth, rdata))
            method_name = list(rdata.keys())[0]
            method = getattr(GDAuth, method_name)
            data = json.loads(method(GDAuth, rdata))
            # logfn1('loginRegister').info(data)
            return Response(data, status=status.HTTP_200_OK)

    # def get(self, request):
        # apiView.info(request.GET)
        # return Response(status=status.HTTP_200_OK)
        # rdata = {request.GET.get('u'):json.loads(request.GET.get('p')), 'request':request}
        # rdata = {decrypt(request.GET.get('u')):decrypt(request.GET.get('p')), 'request':request}
        # logfn1('loginRegister').info(rdata)
        # return Response(data=eval(f'GD.{list(rdata.keys())[0]}')(GD, rdata), status=status.HTTP_200_OK)
        # if self.ddd == 2:
            # return Response(data=json.loads(eval(f'GD.{list(rdata.keys())[0]}')(GD, rdata)), status=status.HTTP_200_OK)
            # return Response(data=encrypt(eval(f'GD.{list(rdata.keys())[0]}')(GD, rdata)), status=status.HTTP_200_OK)
        # elif self.ddd == 1:
            # return Response(data=json.loads(eval(f'GDAuth.{list(rdata.keys())[0]}')(GDAuth, rdata)), status=status.HTTP_200_OK)
            # return Response(data=encrypt(eval(f'GDAuth.{list(rdata.keys())[0]}')(GDAuth, rdata)), status=status.HTTP_200_OK)

    def dispatch(self, request, *args, **kwargs):
        """
        Überprüft, ob `get` oder `get2` aufgerufen werden soll, basierend auf einem
        spezifischen GET-Parameter.
        """
        # if request.method.lower() == 'get' and 'some_condition' in request.GET:
        #     return self.get2(request, *args, **kwargs)
        return super(ApiView, self).dispatch(request, *args, **kwargs)



class GD(SZ, ApiView):
    
    pagination_class = CustomPagination
    @logger.catch
    def LoginRegister(self, vars):
        try:
            from api.authview import Authent
            # logfn1('loginRegister').info(type(vars.get('LoginRegister')))
            # logfn1('loginRegister').info(type(vars.get('LoginRegister').get('filter')))
            if vars.get('LoginRegister').get('filter').get('email'):
                auth = Authent(vars.get('request'), vars.get('LoginRegister').get('filter'))
                res = auth.sendUrl()
                # logfn1('loginRegister').info(vars)
                return json.dumps(res)
            elif vars.get('LoginRegister').get('filter').get('urltoken'):
                auth = Authent(vars.get('request'), vars.get('LoginRegister').get('filter'))
                res = auth.authenticate()
                return json.dumps(res)
            
            return json.dumps(res)
        except Exception as d:
            logfn1('loginRegister').exception(d)
            logfn1('loginRegister').error(d)
    
    def LogOut(self, vars):
        from api.authview import Authent
        auth = Authent(vars.get('request'), vars.get('LogOut').get('filter'))
        res = auth.logout()
        return json.dumps(res)
        
    def GetCategory(self, vars):

        try:
            qs = self.CategoryS.Meta.model.objects.filter(active=True)
            sz = self.CategoryS(qs, many=True)
            return json.dumps(sz.data, cls=DecimalEncoder)
        except Exception as d:
            logfn1('GetCategory').info(d)
    
    def GetBrand(self, vars):
        
        self.BrandS.Meta.fields = ['id','title','slug','category','image','image2','regions', 'active', 'in_stock','products']
        if vars.get("GetBrand").get('filter'):
            qs = self.BrandS.Meta.model.objects.filter(active=True).filter(category__slug=vars.get("GetBrand").get('filter'))
        else:
            self.BrandS.Meta.fields = ['id','title','slug','category','image','image2','regions', 'in_stock']
            qs = self.BrandS.Meta.model.objects.filter(
                Q(active=True) & Q(in_stock=True) 
            )
        # for i in qs:
        #     i.in_stock = True if i.products.filter(qty__gt=0).count() > 0 else False
        #     i.save()
        #     i.active = True if i.products.filter(qty__gt=0).count() > 0 else False
        #     i.save()
        # self.brand.in_stock = True if self.brand.products.filter(qty__gt=0).count() > 0 else False
        # qs = qs.annotate(product_count=Count('product'))
        
        sz = self.BrandS(qs, many=True)
        return json.dumps(sz.data, cls=DecimalEncoder)

    def GetProduct(self, vars):
        self.ProductS.Meta.fields = ['id','brand','value','qty','title','price','image','in_stock','slug','region','currency','description','dcoinprice']
        # self.BrandS.Meta.fields = ['regions','title','image','image2','image', 'category']
        qs = self.ProductS.Meta.model.objects.filter(active=True, qty__gt=0).filter(brand__slug=vars.get("GetProduct").get('filter'))
        
        if not qs:
            return json.dumps({'error':'No products found'}, cls=DecimalEncoder)
        
        region = vars.get("GetProduct").get('region')
        # logfn1('productregions').info(region)
        
        def f():
            if region == 'null':
                return qs.filter(region=qs.first().region)
            elif qs.filter(region=region).first():
                return qs.filter(region=region)
            else:
                reg = qs.first().region
                return qs.filter(region=reg)
        
        sz = self.ProductS(f(), many=True, context={'request':vars.get('request')})
        return json.dumps(sz.data, cls=DecimalEncoder)
      
    # def GetCart(self, vars):
    #     from api.utils.mutations import cart_mutate, get_or_create_cart
    #     self.CartS.Meta.fields = ['id','final_price','order_final_price','process_fee','payment_method_payment','total_products','wallet_payment',\
    #         'payment_method', 'currency', 'products', 'limit', 'rabatt']
    #     cartqs = self.CartS.Meta.model.objects.filter(in_order=False)
        
    #     cart = get_or_create_cart(request=vars.get('request'), cartqs=cartqs)
    #     if vars.get('GetCart'):
    #         cart = cart_mutate(cart, vars)
    #     sz = self.CartS(cart,context={'request':vars.get('request')})
    #     return json.dumps(sz.data, cls=DecimalEncoder)
    
    def GetBasket(self, vars):
        from api.views.basket import BasketCls
        import os
        from api.utils.mutations import get_or_create_basket
        bcl = BasketCls()
        # logfn1('GetBasket','api/views/logs/').debug(bcl)
        # self.BasketS.Meta.fields = ['id','final_price','order_final_price','process_fee','payment_method_payment','total_products','wallet_payment',\
        #     'payment_method', 'currency', 'products', 'limit', 'rabatt']
        basketqs = self.BasketS.Meta.model.objects.filter(in_order=False)
        basket = get_or_create_basket(request=vars.get('request'), basketqs=basketqs)
        if type(basket) == dict:
            return json.dumps(basket)
        if basket.wallet_payment > Decimal(0) and not vars.get('request').user.is_authenticated: basket.wallet_payment = Decimal(0)
        basket.save()
        
        qty = vars.get('GetBasket').get('qty')
        data = bcl.getdata(qty, vars)
        # print(f'data - {data}')
        # print(f'vars - {vars}')
        # product = self.ProductS.Meta.model.objects.filter(id=data.get('id')).first()
        pqs = self.ProductS.Meta.model.objects.filter(active=True)
        ########## remove basket_products if no product id #############
        bplist = list(basket.basket_products.keys())
        if bplist:
            for key in bplist:
                if not pqs.filter(id=key):
                    basket.basket_products.pop(str(key))
                # else:
                #     basket.basket_products.get(str(key))["price"] = float(pqs.filter(id=key).first().price)
            basket.save()
        ################################################################

        product = pqs.filter(id=data.get('id')).first()
        if not product:
            qty = 0
            data = bcl.getdata(qty, vars)

        if data.get('id') and product:
            # product = self.ProductS.Meta.model.objects.filter(id=data.get('id')).first()
            # product = basket.products.filter(id=data.get('id')).first()
            basket.basket_products.update({str(data.get('id')):{'qty':qty, 'price': float(product.price), 'total':float(product.price) * qty}}) 
            vl = list(basket.basket_products.values())
            sm = sum([vl.get('total') for vl in vl])
            res = Decimal(round(Decimal(sm) * basket.currency.price,2))
            sz1 = self.BasketS(basket, context={'request':vars.get('request')})
            l = bcl.sz(sz1, basket)
            # limit = Decimal(sz1.data.get('limit'))
            
            # sz1.data['limit'] = s
            
            if res > l.limit and res > basket.total_price:
                basket.refresh_from_db()
                sz = self.BasketS(basket, context={'request':vars.get('request')})
                l2 = bcl.sz(sz, basket)
            
                # logfn1('GetBasket','api/logs/').info(l2.to_dict()) Shopping cart maximum amount of <i><b class='text-black'> 146.93 Fr. </b></i> has been exceeded."
                dd = {'message':f'Shopping cart maximum amount of {l2.limit} {basket.currency.sign} has been exceeded.',\
                    'type':'warning', 'basket':l2.szdata.to_dict()}
                return json.dumps(dd, cls=DecimalEncoder)
        if data.get('wallet') != None and vars.get('request').user.is_authenticated:
            wallet = self.CoinWalletS.Meta.model.objects.filter(user=vars.get('request').user).first()
            if data.get('wallet') == True:
                if wallet.balance > Decimal(0):
                    # print(f'1 - {basket.wallet_payment == Decimal(0)}')
                    if wallet.balance >= basket.final_price:
                        basket.wallet_payment = basket.final_price
                    else:
                        basket.wallet_payment = wallet.balance
                    basket.save()
                # basket.refresh_from_db()
                basket.save()
            else:
                basket.wallet_payment = Decimal(0)
                basket.save()
                    # return json.dumps({'error':'Insufficient wallet balance'})

        basket.refresh_from_db()
        basket.save(data)
        basket.save()
        sz = self.BasketS(basket, context={'request':vars.get('request')})
        l3 = bcl.sz(sz, basket)
        # limit = Decimal(sz.data.get('limit'))
        # s = (limit + limit*Decimal(0.10)) - basket.total_price
        # sz.data['limit'] = s
        # logfn1('GetBasket','api/logs/').debug(bcl.sz(sz))
        dd = {'message':'', 'type':'', 'basket':l3.szdata.to_dict()}
        if not product and data.get('id'):
            dd = {'message':'Product not available', 'type':'error', 'basket':l3.szdata.to_dict()}
        return json.dumps(dd, cls=DecimalEncoder)
            
    
    def GetCurrency(self, vars):
        qs = self.CurrencyS.Meta.model.objects.filter(active=True)
        
        sz = self.CurrencyS(qs, many=True)
        return json.dumps(sz.data, cls=DecimalEncoder)    
    
    def GetPayment(self, vars):
        qs = self.PaymentS.Meta.model.objects.filter(enabled=True)
        sz = self.PaymentS(qs, many=True)
        return json.dumps(sz.data, cls=DecimalEncoder)    
    
    def GetRegions(self, vars):
        data = list(set(self.BrandS.Meta.model.objects.filter(active=True, products__active=True).values_list('products__region',flat=True)))
        res = list(regionsfn(data))
        sz = {"regions":res}
        return json.dumps(sz)    
    
    def GetSeachBrands(self, vars):
        qs = self.BrandS.Meta.model.objects.filter(eval(vars.get('GetSeachBrands').get('filter')), active=True).annotate(Count('product__region'))
        sz = self.BrandS(qs, many=True)
        return json.dumps(sz.data, cls=DecimalEncoder)
    

class GDAuth(GD,SZ,ApiView):
    
    pagination_class = CustomPagination
    
    
    def GetUser(self, vars):
        # logfn1('userData').info(vars)
        user = vars.get('request').user
        if not user.coinwallet:
                wallet = GDAuth.CoinWalletS.Meta.model()
                wallet.create_user_wallet(user)
        if(vars.get('GetUser').get('mutate') and user.customer.status != 'Verified'):
            # logfn1('userData').info(user)
            # user = self.CustomerS.Meta.model.objects.filter(user=vars.get('request').user).first()
            try:
                if vars.get('GetUser').get('first_name'):
                    user.first_name=vars.get('GetUser').get('first_name')
                if vars.get('GetUser').get('last_name'):
                    user.last_name=vars.get('GetUser').get('last_name')
                if vars.get('GetUser').get('phone'):
                    user.customer.phone=vars.get('GetUser').get('phone')
                if vars.get('GetUser').get('date_of_birth'):
                    user.customer.date_of_birth=vars.get('GetUser').get('date_of_birth')
                if vars.get('GetUser').get('country_code'):
                    user.customer.country_code=vars.get('GetUser').get('country_code')
                if vars.get('GetUser').get('street'):
                    user.customer.street=vars.get('GetUser').get('street')
                if vars.get('GetUser').get('city'):
                    user.customer.city=vars.get('GetUser').get('city')
                if vars.get('GetUser').get('postal_code'):
                    user.customer.postal_code=vars.get('GetUser').get('postal_code')
                user.customer.save()
                user.save()
                qs = user.customer
                sz = self.CustomerS(qs, context={'request':vars.get('request')})
                return json.dumps(sz.data) 
            except Exception as e:
                return json.dumps({'error':str(e)}) 
        else:
            qs = self.CustomerS.Meta.model.objects.filter(user=vars.get('request').user).first()
            sz = self.CustomerS(qs, context={'request':vars.get('request')})
            return json.dumps(sz.data)
    
    @logger.catch
    def GetOrder(self, vars):
        orders = self.OrdersS.Meta.model.objects.filter(basket__owner__user=vars.get('request').user, deleted=False)
        qs = []
        datalist = vars.get('GetOrder').get('datalist')
        if vars.get('GetOrder').get('filter') == 'trash':
            qs.append(True)
            # apiView.info(f'1: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        elif vars.get('GetOrder').get('filter') == 'to_trash':
            for item in datalist.split(','):
                ord = orders.filter(id=item).first()
                ord.trash = True
                ord.save()
            qs.append(False)
            # apiView.info(f'2: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        elif vars.get('GetOrder').get('filter') == 'trashdelete':
            # logfn1('GetOrder','/home/dcback/api/logs').info(f'datalist: {datalist}')
            # logfn1('GetOrder', '/home/dcback/api/logs').info(f"datalist[]: {datalist.split(',')}")
            for item in datalist.split(','):
                ord = orders.filter(id=item).first()
                ord.deleted = True
                ord.save()
            qs.append(True)
            # apiView.info(f'3: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        elif vars.get('GetOrder').get('filter') == 'trashrestore':
            for item in datalist.split(','):
                ord = orders.filter(id=item).first()
                ord.trash = False
                ord.save()
            qs.append(True)
            # apiView.info(f'4: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        else:
            qs.append(False)
            # apiView.info(f'5: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        
        
        def paginated_view(qs,request):
            from rest_framework.renderers import JSONRenderer
            queryset = orders.filter(trash=qs)
            paginator = CustomPagination(vars.get('request'))
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            if paginated_queryset is not None:
                serializer = self.OrdersS(paginated_queryset, many=True, context={'request':request})
                json_data = JSONRenderer().render(serializer.data)
                # apiView.info(json.dumps(paginator.get_paginated_response(json.loads(json_data)).data))
                return json.dumps(paginator.get_paginated_response(json.loads(json_data)).data)
            
            
        return paginated_view(qs[0],vars.get('request'))

    def GetWorder(self, vars):
        
        worders = self.WalletOrderS.Meta.model.objects.filter(owner__user=vars.get('request').user, deleted=False).annotate(ddddddd=F('total_price')*20)
        qs = []
        datalist = vars.get('GetWorder').get('datalist')
        if vars.get('GetWorder').get('filter') == 'trash':
            qs.append(True)
            # apiView.info(f'1: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        elif vars.get('GetWorder').get('filter') == 'toTrash':
            for item in datalist.split(','):
                ord = worders.filter(id=item).first()
                ord.trash = True
                ord.save()
            qs.append(False)
            # apiView.info(f'2: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        elif vars.get('GetWorder').get('filter') == 'trashdelete':
            # logfn1('GetWorders', '/home/dcback/api/logs').info(f'datalist: {datalist}')
            # logfn1('GetWorders', '/home/dcback/api/logs').info(f"datalist[]: {datalist.split(',')}")
            for item in datalist.split(','):
                ord = worders.filter(id=item).first()
                ord.deleted = True
                ord.save()
            qs.append(True)
            # apiView.info(f'3: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        elif vars.get('GetWorder').get('filter') == 'trashrestore':
            for item in datalist.split(','):
                ord = worders.filter(id=item).first()
                ord.trash = False
                ord.save()
            qs.append(True)
            # apiView.info(f'4: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        else:
            qs.append(False)
            # apiView.info(f'5: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        
        
        def paginated_view(qs,request):
            from rest_framework.renderers import JSONRenderer
            queryset = worders.filter(trash=qs)
            paginator = CustomPagination(vars.get('request'))
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            if paginated_queryset is not None:
                serializer = self.WalletOrderS(paginated_queryset, many=True, context={'request':request})
                json_data = JSONRenderer().render(serializer.data)
                # apiView.info(json.dumps(paginator.get_paginated_response(json.loads(json_data)).data))
                return json.dumps(paginator.get_paginated_response(json.loads(json_data)).data)
            
            
        return paginated_view(qs[0],vars.get('request'))
    
    def GetWallet(self, vars):
        trxs = self.WalletS.Meta.model.objects.filter(owner=vars.get('request').user.customer, deleted=False)
        # loggraphql.debug(filter)
        # return Order.objects.filter(customer=info.context.user.customer)
        
        def paginated_view(request):
            from rest_framework.renderers import JSONRenderer
            queryset = trxs.exclude(amount=0.00, balance=0.00, typ="credit")
            paginator = CustomPagination(vars.get('request'))
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            if paginated_queryset is not None:
                serializer = self.WalletS(paginated_queryset, many=True, context={'request':request})
                json_data = JSONRenderer().render(serializer.data)
                # apiView.info(json.dumps(paginator.get_paginated_response(json.loads(json_data)).data))
                return json.dumps(paginator.get_paginated_response(json.loads(json_data)).data)
        return paginated_view(vars.get('request'))
    
    
    def GetCoinWallet(self, vars):
        wallet = self.CoinWalletS.Meta.model.objects.filter(user=vars.get('request').user).first()
        sz = self.CoinWalletS(wallet, context={'request':vars.get('request')})
        return json.dumps(sz.data, cls=DecimalEncoder)
    
    def GetCoinWalletTransaction(self, vars):
        wallet = self.CoinWalletS.Meta.model.objects.filter(user=vars.get('request').user)
        trx = SZ.CoinWalletTransactionS.Meta.model.objects.filter(wallet=wallet.first())
        
        # loggraphql.debug(filter)
        # return Order.objects.filter(customer=info.context.user.customer)
        
        def paginated_view(request):
            from rest_framework.renderers import JSONRenderer
            queryset = trx
            paginator = CustomPagination(vars.get('request'))
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            if paginated_queryset is not None:
                serializer = SZ.CoinWalletTransactionS(paginated_queryset, many=True, context={'request':request})
                json_data = JSONRenderer().render(serializer.data)
                # apiView.info(json.dumps(paginator.get_paginated_response(json.loads(json_data)).data))
                return json.dumps(paginator.get_paginated_response(json.loads(json_data)).data)
        return paginated_view(vars.get('request'))
    
    
    def GetCoinWalletDeposit(self, vars):
        depositqs = self.CoinWalletDepositS.Meta.model.objects.filter(coinwallet__user=vars.get('request').user)
        qs = []
        datalist = vars.get('GetCoinWalletDeposit').get('GetCoinWalletDeposit')
        if vars.get('GetCoinWalletDeposit').get('filter') == 'trash':
            qs.append(True)
            # apiView.info(f'1: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        elif vars.get('GetCoinWalletDeposit').get('filter') == 'to_trash':
            for item in datalist.split(','):
                ord = depositqs.filter(id=item).first()
                ord.trash = True
                ord.save()
            qs.append(False)
            # apiView.info(f'2: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        elif vars.get('GetCoinWalletDeposit').get('filter') == 'trashdelete':
            # logfn1('GetOrder','/home/dcback/api/logs').info(f'datalist: {datalist}')
            # logfn1('GetOrder', '/home/dcback/api/logs').info(f"datalist[]: {datalist.split(',')}")
            for item in datalist.split(','):
                ord = depositqs.filter(id=item).first()
                ord.deleted = True
                ord.save()
            qs.append(True)
            # apiView.info(f'3: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        elif vars.get('GetCoinWalletDeposit').get('filter') == 'trashrestore':
            for item in datalist.split(','):
                ord = depositqs.filter(id=item).first()
                ord.trash = False
                ord.save()
            qs.append(True)
            # apiView.info(f'4: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        else:
            qs.append(False)
            # apiView.info(f'5: {qs}')
            # return get_paginator(qs, page_size, page, OrdersPaginatedType)
        
        
        def paginated_view(qs,request):
            from rest_framework.renderers import JSONRenderer
            queryset = depositqs.filter(trash=qs)
            paginator = CustomPagination(vars.get('request'))
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            if paginated_queryset is not None:
                serializer = self.CoinWalletDepositS(paginated_queryset, many=True, context={'request':request})
                json_data = JSONRenderer().render(serializer.data)
                # apiView.info(json.dumps(paginator.get_paginated_response(json.loads(json_data)).data))
                return json.dumps(paginator.get_paginated_response(json.loads(json_data)).data)
            
            
        return paginated_view(qs[0],vars.get('request'))
    
    @logger.catch
    def OrderSend(self, vars):
        from eshop.payment.getpayment import getPayment
        from eshop.Orders.order import Order
        from eshop.Utilss.utils import limitcheck
        from api.orderprocess import processOrder
        
        args = vars.get('OrderSend')
        request = vars.get('request')
        limitres = limitcheck(request)

        if args.get('oid'):
            r = processOrder(args.get('oid'))
            return r

        if limitres:
            return json.dumps({'detail': limitres+'_limit', 'message': limitres.capitalize()+' limit exceeded. '
                                                    'Please reduce the shopping cart or try again later.', 'v':request.user.customer.status, 'type':'warning'})
        try:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        except:
            ip = request.META['REMOTE_ADDR']

        # logfn1('orderSend').info(res)
        # sleep(50)
        # return json.dumps({'type':'success', 'step':f'Order Created ID: {ip}'})
        order = Order()
        # logfn1('orderSend','api/logs/').info(vars)
        res = order.create(request, args.get('del_email'))
        # logfn1('orderSend','api/logs/').info(res)
        # logfn1('orderSend','api/logs/').info(res.uuid)
        if res.uuid:
            try:
                resp = getPayment(request, res)
            except Exception as d:
                logfn1('orderSend','api/logs/').info(d)
        return json.dumps(resp)
    
    
    def GetSonst(self, vars):
        if vars.get('GetSonst').get('op') == 'o_m_resend':
            try:
                oid = vars.get('GetSonst').get('oid')
                if redischeck(oid) == 0:
                    return json.dumps({'type':'warning', 'message':'''<div>Too many requests. Please try later.</div>'''})
                r = orderemail(oid)
                if r == 1:
                    msg = f"<div>Email for order <b>#{oid}</b> resent successfully.</div>"
                    return json.dumps({'type':'success', 'message': msg})
                else:
                    msg = f"Failed to resend Email for order <b>#{oid}</b>. Please try again later."
                    return json.dumps({'type':'error', 'message': msg})
            except Exception as d:
                return json.dumps({'type':'error', 'message':f'{d} - GENERAL ERROR 2323'})
        if vars.get('GetSonst').get('op') == 'verifi':
            from eshop_api.main.views import VerifView
            res = VerifView.post(VerifView, vars.get('request'))
            if res.startswith('http'):
                type = 'success,url'
            else:
                type = 'error'
            return json.dumps({'type':type, 'message':res})
    
        

