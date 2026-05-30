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
import json
from .flexepin.flexepin import Flexepin
from .utils_payment import BlList



{
  "transaction_id": "87438239",
  "trans_no": "28937482",
  "result": 0,
  "result_description": "Success",
  "serial": "53001000000000001",
  "value": 10,
  "cost": 9.7,
  "currency": "CAD",
  "status": "USED",
  "description": "Flexepin CAD 10.00",
  "ean": "9350233001017"
}

class PaymentGate(APIView):

    def post(self, request):

        if request.data and request.data.get('name') == 'Flexepin':
            
            fp = Flexepin()
            terminalId = 'digicod.eu'
            
            if request.data.get('action') == 'status':
                return Response(fp.do_private_query('GET', 'status', None).json())
            
            elif request.data.get('action') == 'validate':
                transId = fp.random_code(length=16, low=False, spchr=False)
                pin = request.data.get('pin')
                ip = request.META.get('HTTP_X_FORWARDED_FOR')
                fprint = request.COOKIES.get('_polz')

                bl = BlList(ip,fprint,1,5,30,'fpvalid_1')
                bch = bl.bl_create().get('blocked')
                if bch:
                    return Response({"result_description": f'''Too many validation attempts! Voucher 
                                     validation is temporarily blocked until {bch.strftime('%d.%m.%Y %H:%M:%S')} UTC'''})

                bl2 = BlList(ip,fprint,30,20,120,'fpvalid_2')
                bch = bl2.bl_create().get('blocked')
                if bch:
                    return Response({"result_description": f'''Too many validation attempts! Voucher
                                    validation is temporarily blocked until {bch.strftime('%d.%m.%Y %H:%M:%S')} UTC'''})

                res = fp.do_private_query('GET', 'voucher/validate/{0}/{1}/{2}'.format(pin, terminalId, transId), None).json()
                keys = ['cost','ean','serial','trans_no','transaction_id']
                for key in keys:
                    try:
                        del res[key]
                    except:
                        continue
                return Response(res)
            
            elif request.data.get('action') == 'redeem':
                from eshop.productorder.prodOrder import ProdOrder
                customer_ip = request.META.get('HTTP_X_FORWARDED_FOR')
                transId = request.data.get('orderid')
                pin = request.data.get('fpin')
                res = fp.do_private_query('PUT', 'voucher/redeem/{0}/{1}/{2}'.format(pin, terminalId, transId), {"customer_ip":customer_ip}).json()
                if res.get('result_description') == "Success":
                    order = Order.objects.filter(id=request.data.get('orderid')).first()
                    order.responsedata = res
                    order.save()
                    if order.pay_amount < decimal.Decimal(res.get("value")):
                        amount = (decimal.Decimal(res.get("value")) - order.pay_amount) / order.cart.currency.price
                        wallet_transaction(order.customer, 'credit', round(amount-amount*decimal.Decimal(0.06),2),
                                            f'Remaining credit from order #{order.id}')
                    po = ProdOrder(order)
                    po.do_prod_order()
                    return Response({"detail": "OK", "url": f'/myaccount/?myorders'})
                else:
                    return Response({"detail": "error", **res})
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
