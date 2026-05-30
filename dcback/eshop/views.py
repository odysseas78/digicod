from asyncio import DefaultEventLoopPolicy
import os
import secrets
import time
from django_filters.rest_framework import DjangoFilterBackend
from pytz import utc
from django.db.models import Q
from rest_framework import filters
from datetime import datetime, timezone, timedelta
from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework import status, generics
from rest_framework.decorators import APIView, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from eshop.models import Order, Orders, Verification, WalletOrder, Wallet, Currency, Payment, ProductCode, Customer
from eshop.serializers import WalletSerializer, WalletOrderSerializer
from eshop.Utilss.utils import check_process_order, json_read, json_save, wolimitcheck
from eshop_api.main.serializers import ProductCodeSerializer
from eshop_api.utils import create_login_stat
from django.conf import settings
from loguru import logger
import json, jsons
from eshop_api.pagination import OrdersPagination
import decimal
from django.shortcuts import redirect
import requests

BASE_DIR = settings.BASE_DIR
ENV_DICT = settings.ENV_DICT

# def checkadmin(request):
#     from config.urls import urlpatterns, adminpaths
#     if request.headers.get('Cookie'):
#         for t in request.headers.get('Cookie').split(' '):
#             if 'toooken' in t:
#                 token = Token.objects.filter(key=t.split('=')[1]).first()
#                 if token and token.user.is_superuser:
#                     urlpatterns += adminpaths
#                     return True
#     return False


def logfn1(name,path='logs/'):
    logger.add(f"{path}/{name}.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == name)
    return logger.bind(name=name)

def returncheck(request, orderid):
    if request.method == 'POST':
        order = Order.objects.filter(id=orderid).first()
        worder = WalletOrder.objects.filter(id=orderid).first()
        if order:
            if order.status == 'pending_payment':
                i = 0
                while i < 15 and order.status == 'pending_payment':
                    check_process_order(request, order, worder)
                    time.sleep(1)
                    i += 1
            return HttpResponse('/myaccount/?myorders')
        elif worder:
            if worder.status == 'pending_payment':
                i = 0
                while i < 15 and worder.status == 'pending_payment':
                    check_process_order(request, order, worder)
                    time.sleep(1)
                    i += 1
            return HttpResponse('/myaccount/?mywallet')
        else:
            return HttpResponse('/')

    if request.method == 'GET':
        return render(request, BASE_DIR / 'cdnx/eshop-ui/build/index.html')
# #-----------------------------------------------------------------------------------
def view_404(request, exception=None):
    # make a redirect to homepage
    # you can use the name of url or just the plain link
    return render(request, BASE_DIR / 'cdnx/eshop-ui/build/index.html')

# @logger.catch
@require_http_methods(["POST"])
def callbck(request, orderid):
    logfn1("callback",path='api/logs/').info(orderid)
    logfn1("callback",path='api/logs/').info(json.loads(request.POST))
    logfn1("callback",path='api/logs/').info(json.loads(request.body))
    # try:
    #     data = json_read('/home/dcback/eshop/cb_data.json')
    #     data.update({str(datetime.now()): {'orderId': str(orderid), 'callback': request.POST}})
    #     json_save(data, '/home/dcback/eshop/cb_data.json')
    # except Exception as d:
    #     send_mail(str(orderid), str(d), 'order@digicod.eu', ['info@digicod.eu'], fail_silently=False)
    # callbck_log.info('orderid: '+str(orderid))
    # callbck_log.info(request.headers)
    # return HttpResponse(json.loads(bytes.decode(request.body)))
    if orderid == 111000:
        data = json.loads(request.body)
        # callbck_log.info('orderid: '+str(orderid))
        # callbck_log.info(request.headers)
        # callbck_log.info(f'start: {data}')
        veriqs = Verification.objects.filter(verification_id=data.get('verification_id')).first()
        customer = Customer.objects.filter(applicant_id=data.get('applicant_id')).first()
        if data.get('type') == 'VERIFICATION_STATUS_CHANGED':
            # callbck_log.info(f"data.get('verification_status': {data.get('verification_status')}")
            if data.get('verification_status') == 'pending':
                customer.status = 'Under Review'
                customer.save()
                return HttpResponse(status=status.HTTP_205_RESET_CONTENT)
            return HttpResponse(status=status.HTTP_205_RESET_CONTENT)
                
        # callbck_log.info(f"data.get('type'): {data.get('type')}")
        if data.get('type') == 'VERIFICATION_COMPLETED' and data.get('status') == 'completed':
            # callbck_log.info(f"data.get('verified') == True: {data.get('verified') == True}")
            if data.get("verified") == True:
                # callbck_log.info(f"customer: {customer} - applicant_id: {customer.applicant_id})")
                veriqs.status = 'completed'
                veriqs.result = 'verified'
                customer.country_code = data.get('applicant').get('addresses')[0].get('country').lower()
                # callbck_log.info(f"data.get('applicant').get('addresses')[0].get('street_name'): {data.get('applicant').get('addresses')[0].get('street_name')})")
                customer.street = data.get('applicant').get('addresses')[0].get('street_name')
                customer.city = data.get('applicant').get('addresses')[0].get('city')
                customer.postal_code = data.get('applicant').get('addresses')[0].get('postal_code')
                customer.status = 'Verified'
                customer.rolle = 'regular'
                customer.date_of_birth = data.get('applicant').get('dob')
                veriqs.save()
                customer.save()
                customer.user.first_name = data.get('applicant').get('first_name')
                customer.user.last_name = data.get('applicant').get('last_name')
                customer.user.save()
                return HttpResponse(status=status.HTTP_205_RESET_CONTENT)
            else:
                veriqs.status = 'completed'
                veriqs.result = 'invalid'
                customer.status = 'Unverified'
                customer.rolle = 'new'
                veriqs.save()
                customer.save()
                return HttpResponse(status=status.HTTP_205_RESET_CONTENT)
                
        else:
            return HttpResponse(status=status.HTTP_205_RESET_CONTENT)
        
    if orderid == 110033:
        data2 = json_read('/home/dcback/eshop/cb_data2.json')
        data2.update({str(datetime.now()): json.loads(request.body)})
        json_save(data2, '/home/dcback/eshop/cb_data2.json')
        if(json.loads(request.body).get('transaction') and json.loads(request.body).get('transaction').get('order')):
            oid = json.loads(request.body).get('transaction').get('order').get('id')
            order = Order.objects.filter(id=oid).first()
            worder = WalletOrder.objects.filter(id=oid).first()
            if (order and order.status == 'pending_payment') or (worder and worder.status == 'pending_payment'):
                check_process_order(request, order, worder)
        return HttpResponse(status=status.HTTP_200_OK)
        
    try:
        # callbck_log.info(f'Neosurf and REST request.body: {request.body}')
        order = Order.objects.filter(id=orderid).first()
        worder = WalletOrder.objects.filter(id=orderid).first()
        if (order and order.status == 'pending_payment') or (worder and worder.status == 'pending_payment'):
            check_process_order(request, order, worder)
        data = json_read('/home/dcback/eshop/cb_data.json')
        data.update({str(datetime.now()): json.loads(json.dumps(request.POST))})
        json_save(data, '/home/dcback/eshop/cb_data.json')
    except Exception as d:
        pass
    return HttpResponse(status=status.HTTP_200_OK)
    # return Response({'malakies': True, 'prprprprp': False})


class WalletViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletSerializer
    queryset = Wallet.objects.all()
    pagination_class = OrdersPagination

    
    # @logger.catch
    # @action(methods=["get"], detail=False)
    # def current_customer_wallet(self, request):
    #     # print(request.user.customer)
    #     qs = Wallet.objects.filter(owner=request.user.customer)
    #     serializer = self.get_serializer(qs, many=True)
    #     serializer_data = serializer.data
    #     # if request.user.is_authenticated:
    #     return Response(serializer_data)


    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(owner=request.user.customer)
        return super().list(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    # @action(methods=["get"], detail=False)
    # def wallet_transactions(self, request, *args, **kwargs):
    #     wallet = Wallet.objects.filter(owner=request.user.customer)
    #     if wallet:
    #         wallet = Wallet.objects.get(owner=request.user.customer)
    #         transactions = Transaction.objects.filter(wallet=wallet)
    #         queryset = self.filter_queryset(transactions)
    #         serializer = TransactionSerializer(queryset, many=True)
    #         return Response(serializer.data)
    #     else:
    #         return Response({'detail': 'not fund'})


class WalletOrderView(ModelViewSet):

    queryset = WalletOrder.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = WalletOrderSerializer
    pagination_class = OrdersPagination
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['id']
    search_fields = ['id']


    def list(self, request, *args, **kwargs):
        if request.GET.get('worder') == 'all':
            self.queryset = self.queryset.filter(status='pending_payment', currency__type='crypto')
        else:
            self.queryset = self.queryset.filter(owner=request.user.customer)
        return super().list(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     try:
    #         if request.GET.get('woid'):
    #             try:
    #                 qs = WalletOrder.objects.filter(id=request.GET['woid'])
    #                 serializer = WalletOrderSerializer(qs, many=True)
    #                 return Response(serializer.data)
    #             except:
    #                 return Response(status=status.HTTP_400_BAD_REQUEST)
    #         elif request.GET.get('worder') == 'all':
    #             qs = WalletOrder.objects.filter(status='pending_payment', currency__type='crypto')
    #             serializer = WalletOrderSerializer(qs, many=True)
    #             return Response(serializer.data)
    #         else:
    #             try:
    #                 qs = WalletOrder.objects.filter(owner=request.user.customer)
    #                 serializer = WalletOrderSerializer(qs, many=True)
    #                 return Response(serializer.data)
    #             except:
    #                 return Response(status=status.HTTP_400_BAD_REQUEST)
    #     except:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        # return Response(request.data)
        order = self.queryset.filter(id=request.data.get('id')).first()
        request.data.get('json')['txid'] = list(set(request.data.get('json').get('txid')))
        order.json.update(request.data.get('json'))
        order.save()
        return Response(status=status.HTTP_201_CREATED)


    def create(self, request, *args, **kwargs):
        curr = Currency.objects.filter(shortname=request.data['currency']).first()
        res = wolimitcheck(request, curr)
        if res:
            return Response({'detail': res+'_limit', 'message': res.capitalize()+' limit exceeded. \
                                                        Please reduce top-up amount or try again later.', 'v':request.user.customer.status})
        try:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        except:
            ip = request.META['REMOTE_ADDR']
        dg = 8
        if curr.type == 'fiat':
            dg = 2
        if curr.shortname == 'USDT':
            dg = 4
        payment = Payment.objects.filter(name=request.data['payment_method']).first()
        totalprice = decimal.Decimal(request.data['total_price'])
        price = round((totalprice / (payment.fee_rate+100) * 100) - payment.fee_fix * curr.price, dg)
        request.data['curprice'] = str(curr.price)
        lk = WalletOrder.objects.create(
            owner=request.user.customer,
            price=price,
            fee=totalprice - price,
            total_price=totalprice,
            currency=curr,
            payment_method=payment,
            payoption=payment.payoptions.filter(id=request.data.get('payoption')).first(),
            json=request.data,
            ip=ip
            )
        if lk:
            serializer = self.serializer_class(lk, many=False)
        # if serializer.is_valid():
        #     obj = serializer.save()
            # obj.category.set(cat)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return super().create(request, *args, **kwargs)


    # def post(self, request, *args, **kwargs):
    #     curr = Currency.objects.filter(shortname=request.data['currency']).first()
    #     res = wolimitcheck(request, curr)
    #     if res:
    #         return Response({'detail': res+'_limit', 'message': res.capitalize()+' limit exceeded. \
    #                                                     Please reduce top-up amount or try again later.', 'v':request.user.customer.status})
    #     try:
    #         ip = request.META['HTTP_X_FORWARDED_FOR']
    #     except:
    #         ip = request.META['REMOTE_ADDR']
    #     dg = 8
    #     if curr.type == 'fiat':
    #         dg = 2
    #     if curr.shortname == 'USDT':
    #         dg = 4
    #     payment = Payment.objects.filter(name=request.data['payment_method']).first()
    #     totalprice = decimal.Decimal(request.data['total_price'])
    #     price = round((totalprice / (payment.fee_rate+100) * 100) - payment.fee_fix * curr.price, dg)
    #     lk = WalletOrder.objects.create(
    #         owner=request.user.customer,
    #         price=price,
    #         fee=totalprice - price,
    #         total_price=totalprice,
    #         currency=curr,
    #         payment_method=payment,
    #         payoption=payment.payoptions.filter(id=request.data.get('payoption')).first(),
    #         ip=ip
    #         )
    #     try:
    #         create_login_stat(username=request.user.username,
    #                           ip=ip,
    #                           result=lk.id, useragent=request.META.get('HTTP_USER_AGENT'),
    #                           device=request.META.get('HTTP_SEC_CH_UA_PLATFORM'),
    #                           meta=request.META)
    #     except:
    #         pass
    #     # qs = self.filter_queryset(lk)
    #     serializer = WalletOrderSerializer(lk, many=False)
    #     return Response(serializer.data)



class ProductCodeView(generics.ListAPIView):

    queryset = ProductCode.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductCodeSerializer

    # def get(self, request, *args, **kwargs):

# @logger.catch
def cancel(request, ouuid):
    oqs = Orders.objects.filter(uuid=ouuid, status='pending_payment').first()
    # woqs = WalletOrder.objects.filter(id=ouuid, status='pending_payment').first()
    if oqs:
        oqs.status = 'cancelled'
        oqs.save()
        return redirect('/account')
    return redirect('/account')



def kinguin_wh(request, type):
    from kinguin.products import getprod
    # logger.add("logs/kinguin_log.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "kinguin_log")
    # kinguin_log = logger.bind(name="kinguin_log")
    if type == 'update':
        if request.headers.get("X-Event-Secret") == ENV_DICT.kinguin_hook_secret:
            data = json.loads(request.body)
            getprod(prodid=data.get('productId'))
    return HttpResponse(status=status.HTTP_204_NO_CONTENT)


def binance_wh(request):
    if request.body:
        try:
            body = json.loads(request.body)
            
            if body.get('bizType') == 'PAY':
                data = json.loads(body.get('data'))
                order = Order.objects.filter(id=data.get('merchantTradeNo')).first()
                worder = WalletOrder.objects.filter(id=data.get('merchantTradeNo')).first()
                if order:
                    if order.status == 'pending_payment':
                        i = 0
                        while i < 15 and order.status == 'pending_payment':
                            check_process_order(request, order, worder)
                            time.sleep(1)
                            i += 1
                elif worder:
                    if worder.status == 'pending_payment':
                        i = 0
                        while i < 15 and worder.status == 'pending_payment':
                            check_process_order(request, order, worder)
                            time.sleep(1)
                            i += 1
        except Exception as d:
            logfn1("binance_wh").exception(d)

    return HttpResponse(json.dumps({"returnCode":"SUCCESS", "returnMessage":None}), status=status.HTTP_200_OK)


class SocialLoginView(APIView):
    
    def getOrCreateUser(self, request=None, resp=None):
        from eshop.models import User, Customer
        if not resp and request:
            user, create = User.objects.get_or_create(
            email=request.data.get('email'),
            defaults={
                    "username":request.data.get('email'),
                    }
            )
            if create:
                customer, create2 = Customer.objects.get_or_create(
                    user=user,
                    defaults={
                        'rolle':'new',
                        'status':'Unverified',
                        }
                )
        else:
            firstname = resp.get('given_name') if resp.get('given_name') else ''
            lastname = resp.get('family_name') if resp.get('family_name') else ''
            user, create = User.objects.get_or_create(
                email=resp.get('email'),
                defaults={
                        "username":resp.get('email'),
                        "first_name":firstname,
                        "last_name":lastname
                        }
            )
            if create:
                customer, create2 = Customer.objects.get_or_create(
                    user=user,
                    defaults={
                        'rolle':'new',
                        'status':'Unverified',
                        'json':resp
                        }
                )
            else:
                user.customer.json = resp
                user.customer.save()
                user.save()
                if not user.first_name and resp.get('given_name'):
                    user.first_name = resp.get('given_name')
                    user.save()
                if not user.last_name and resp.get('family_name'):
                    user.last_name = resp.get('family_name')
                    user.save()
        return user
    
    def post(self, request):
        logger.add("logs/social_login_log.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "socLogin_log")
        socLogin_log = logger.bind(name="socLogin_log")
        from djoser.utils import login_user
        from eshop.models import UrlToken
        if request.data.get('access_token'):
            header = {
                "Authorization": f"Bearer {request.data.get('access_token')}",
                "Accept": 'application/json'
            }
            resp = requests.get(f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={request.data.get('access_token')}", headers=header).json()
            token = login_user(request, self.getOrCreateUser(resp=resp))
        elif request.data.get('email'):
            user = self.getOrCreateUser(request=request)
            if user:
                try:
                    qs = UrlToken.objects.filter(Q(created_at__lte=(datetime.now(utc) - timedelta(minutes=15))) | Q(customer__user__email=request.data.get('email')))
                    qs.delete()
                except Exception as d:
                    socLogin_log.exception(d)
                urltoken = secrets.token_urlsafe(64)
                create = UrlToken(customer=user.customer, token=urltoken)
                create.save()
                html_email = f'''
                    <p> Please go to the following page to login:
                    <a href={request.build_absolute_uri('/')+'email_login/0/'+create.token} >
                    {request.build_absolute_uri('/')+'email_login/0/'+create.token}
                    </a>
                    </p>
                    <p>The link is valid for 15 minutes.</p>
                    <p>Thanks for using our site!</p>
                    <p>The {request.build_absolute_uri('/')[8:-1]} team.</p>
                    '''
                message = html_email
                subject, from_email, to = f"Login to your account", '"DIGICOD" <support@digicod.eu>', request.data.get('email')
                text_content = f'Login to your account {request.build_absolute_uri("/")+create.token}'
                html_content = message
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                return Response({'email':user.email,'message': 'An email was sent successfully. Please follow the instructions in the email.'})
            else:
                return Response({'message': 'Something went wrong.'})
        elif request.data.get('uid') and request.data.get('token'):
            try:
                qs = UrlToken.objects.filter(Q(created_at__gt=(datetime.now(utc) - timedelta(minutes=15))) & Q(token=request.data.get('token'))).first()
            except Exception as d:
                socLogin_log.exception(d)
            if qs:
                token = login_user(request, qs.customer.user)
                qs.delete()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'Expired'})
        return Response({"auth_token":token.key})
    
    
    
    
    
class TestView(ModelViewSet):

    

    def list(self, request, *args, **kwargs):
        
        
        
        return Response('response')
        # if request.GET.get('worder') == 'all':
        #     self.queryset = self.queryset.filter(status='pending_payment', currency__type='crypto')
        # else:
        #     self.queryset = self.queryset.filter(owner=request.user.customer)
        # return super().list(request, *args, **kwargs)
