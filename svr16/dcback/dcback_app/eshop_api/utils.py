import hashlib
import os
import json
import re
from collections import OrderedDict
from datetime import datetime, timezone, timedelta
import time
from loguru import logger
from django.core.mail import send_mail
from eshop.models import Cart, Verification, Wallet, Order, WalletOrder
from apps.accounts.models import *
from django.db.models import Q

from rest_framework.response import Response
import requests
# import socket
# import socks
# if os.environ.get('DOMAIN') == 'https://www.digicod.eu':
#     ip='127.0.0.10' # change your proxy's ip
#     port = 6000 # change your proxy's port
#     socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
#     socket.socket = socks.socksocket


# logger.add("eshop_api_utils.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "utils")
utilslog = logger.bind(name="utils")
class Verify():
    # token = os.environ.get('kycaid_test_api')
    
    def del_address(address_id, test):
        if test == True:
            token = vault_Client.get_secret('kycaid', 'kycaid_test_api')
        elif test == False:
            token = vault_Client.get_secret('kycaid', 'kycaid_api')
        apiurl = f"https://api.kycaid.com/addresses/{address_id}"
        resp = requests.delete(apiurl, headers={'Authorization': f'Token {token}'})
        return resp
    
    def del_document(document_id, test):
        if test == True:
            token = vault_Client.get_secret('kycaid', 'kycaid_test_api')
        elif test == False:
            token = vault_Client.get_secret('kycaid', 'kycaid_api')
        apiurl = f"https://api.kycaid.com/documents/{document_id}"
        resp = requests.delete(apiurl, headers={'Authorization': f'Token {token}'})
        return resp
    
    def get_applicant(applicant_id, test):
        if test == True:
            token = vault_Client.get_secret('kycaid', 'kycaid_test_api')
        elif test == False:
            token = vault_Client.get_secret('kycaid', 'kycaid_api')
        apiurl = f"https://api.kycaid.com/applicants/{applicant_id}"
        resp = requests.get(apiurl, headers={'Authorization': f'Token {token}'})
        return resp
    
    
    def get_verifications(verification_id, test):
        if test == True:
            token = vault_Client.get_secret('kycaid', 'kycaid_test_api')
        elif test == False:
            token = vault_Client.get_secret('kycaid', 'kycaid_api')
        apiurl = f"https://api.kycaid.com/verifications/{verification_id}"
        resp = requests.get(apiurl, headers={'Authorization': f'Token {token}'})
        return resp
    
    
    def start(request, test):
        if test == True:
            token = vault_Client.get_secret('kycaid', 'kycaid_test_api')
        elif test == False:
            token = vault_Client.get_secret('kycaid', 'kycaid_api')
        
        # CREATE APPLICANT ################
        if not request.user.customer.applicant_id:
            post_data = {
                    "type": "PERSON",
                    # "first_name": request.user.first_name,
                    # "last_name": request.user.last_name,
                    # "dob": request.user.customer.date_of_birth,
                    # "residence_country": "GB",
                    "email": request.user.email,
                    "external_applicant_id": request.user.id
                }
            apiurl = "https://api.kycaid.com/applicants"
            resp = requests.post(apiurl, data=post_data, headers={'Authorization': f'Token {token}'}).json()
            if resp and resp.get('applicant_id'):
                request.user.customer.applicant_id = resp.get('applicant_id')
                request.user.customer.save()
            else:
                return Response({'detail': 'Something went wrong! Please try again.'})
                
        # GET LINK ################
        post_data = {
                    "applicant_id": request.user.customer.applicant_id,
                    "language_code": "EN"
                }
        apiurl = f"https://api.kycaid.com/forms/{vault_Client.get_secret('kycaid', 'kycaid_form_main')}/urls"
        resp = requests.post(apiurl, data=post_data, headers={'Authorization': f'Token {token}'})
        return resp
    
    def calbck_recheck():
        from eshop.models import Customer, Verification
        qs = Customer.objects.filter(status='Under Review')
        if qs.count() > 0:
            for customer in qs:
                data = Verify.get_applicant(customer.applicant_id, True).json()
                if data.get('verification_status') == "valid":
                    veriqs = Verification.objects.filter(customer=customer).first()
                    veriqs.status = 'completed'
                    veriqs.result = 'verified'
                    customer.country_code = data.get('addresses')[0].get('country').lower()
                    customer.street = data.get('addresses')[0].get('street_name')
                    customer.city = data.get('addresses')[0].get('city')
                    customer.postal_code = data.get('addresses')[0].get('postal_code')
                    customer.status = 'Verified'
                    customer.rolle = 'regular'
                    customer.date_of_birth = data.get('dob')
                    veriqs.save()
                    customer.save()
                    customer.user.first_name = data.get('first_name')
                    customer.user.last_name = data.get('last_name')
                    customer.user.save()
                else:
                    veriqs = Verification.objects.filter(customer=customer).first()
                    resp = Verify.get_verifications(veriqs.verification_id, False).json()
                    if resp['status'] == 'completed':
                        veriqs.status = 'completed'
                        veriqs.result = 'invalid'
                        customer.status = 'Unverified'
                        customer.rolle = 'new'
                        veriqs.save()
                        customer.save()
                    if resp['status'] == 'unused':
                        veriqs.status = 'unused'
                        customer.status = 'Unverified'
                        customer.rolle = 'new'
                        veriqs.save()
                        customer.save()
    
    def post(self, request):
        verifi = logger.bind(name="verifi")
        import base64
        from base64 import b64encode, b64decode
        
        vqs = Verification.objects.filter(customer=request.user.customer).filter(status=None).last()
        if vqs:
            verif = self.get_verifications(vqs.verification_id, test=False).json()
            if verif and verif.get('status') and verif.get('status') == 'unused':
                request.user.customer.status = 'Under Review'
                request.user.customer.save()
                return Response ({'form_url': vqs.form_url})
        
        res = self.start(request, test=False).json()
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
                return Response ({'form_url': res.get('form_url')}, status=status.HTTP_200_OK)
            else:
                return Response({'detail':'There has been an error. Please try again.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        else:
            return Response({'detail':'There has been an error. Please try again.'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    

def get_cart_and_products_in_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(in_order=False, for_anonymous_user=False, owner=request.user.customer).first()
        products_in_cart = [cp.product.id for cp in cart.products.all()]
        # products_in_cart = products_in_cart.order_by('id')
        return cart, products_in_cart
    return 0, 0


def neosurf_pay_send(orderqs, id, amount, currency, test, urlOk, urlKo, urlPending, urlCallback):
    # request.data['location'] + "/order_detail/" + str(orderid)
    # request.data['location'] + "/checkout/"
    #request.data['location'] + "/callbck/" + str(orderid) + '/'
    if test == 'yes':
        id = 'T'+str(id)
    expiry = (datetime.now(timezone.utc) + timedelta(minutes=120)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    amount = int(float(round(amount, 2)) * 100)
    order = {'amount': str(amount), 'currency': currency, 'expiry': expiry, 'hash': "",
             'language': "en", 'merchantId': "24738", 'merchantTransactionId': str(id),
             'prohibitedForMinors': "no", 'subMerchantId': "digicod.eu", 'test': test,
             'urlOk': urlOk, 'urlKo': urlKo, "urlPending": urlPending,
             "urlCallback": urlCallback, "version": "3"
             }
    order = OrderedDict(sorted(order.items()))
    ordstr = ''.join(order.values()) + "5f9a28c298aa7fda52964e3643d79270"
    h = ordstr.encode()
    hashk = hashlib.sha512(h).hexdigest()
    order["hash"] = hashk
    post_data = json.dumps(order, separators=(',', ':'))
    orderqs.postdata = post_data
    orderqs.save()
    i=0
    statuscode = 504
    while statuscode >= 500 and statuscode <= 504 and i < 6:
        resp = requests.post("https://pay.neosurf.com", data=post_data, headers={'content-type': 'application/json'})
        i += 1
        statuscode = resp.status_code
        time.sleep(2)
    try:
        url_pattern = r'https://[\S]+'
        urls = re.findall(url_pattern, resp.text)
        url = urls[2][:-2]
        return {"detail": "OK", "url": url}
    except:
        return {"detail": "fault", "message": 'There has been an error. Try again later or contact support. (NSF)'}


def callbck_check(request):
    order = {'amount': request.POST.get("amount"), 'created': request.POST.get("created"),
             'currency': request.POST.get("currency"), 'errorCode': request.POST.get("errorCode"),
             'errorMessage': request.POST.get("errorMessage"), 'merchantId': request.POST.get("merchantId"),
             'merchantTransactionId': request.POST.get("merchantTransactionId"), 'methodChargedAmount': request.POST.get("methodChargedAmount"),
             'methodCurrency': request.POST.get("methodCurrency"), 'methodExpiry': request.POST.get("methodExpiry"),
             'methodId': request.POST.get("methodId"), 'methodLabel': request.POST.get("methodLabel"),
             'methodName': request.POST.get("methodName"), 'status': request.POST.get("status"),
             'subMerchantId': request.POST.get("subMerchantId"), 'transaction3d': request.POST.get("transaction3d"),
             'transactionId': request.POST.get("transactionId")
             }
    order = OrderedDict(sorted(order.items()))
    ordstr = ''.join(order.values()) + "5f9a28c298aa7fda52964e3643d79270"
    h = ordstr.encode()
    hashk = hashlib.sha512(h).hexdigest()
    return hashk


def wallet_transaction(owner, type, amount, description):
    wallet = Wallet.objects.filter(owner=owner)
    if wallet.first().balance < -amount and type == 'debit':
        send_mail(
            'Wallet error',
            'Wallet error',
            'order@digicod.eu',
            ['admin@digicod.eu'],
            fail_silently=False,
        )
        return None
    tr = Wallet.objects.create(
        owner=owner,
        typ=type,
        amount=amount,
        description=description
    )
    return tr


def get_geopos(ip):
    # resp = requests.get(f'http://api.ipapi.com/api/{ip}?access_key=2abbbfcc49581fafa95fc3e2e4f34e55').json()
    resp = requests.get(f'https://api.ipgeolocation.io/ipgeo?apiKey=69be3a252f95412296a93db9f7dcc6a3&ip={ip}').json()
    # resp = f'https://api.bigdatacloud.net/data/ip-geolocation?ip={ip}&localityLanguage=en&key=bdc_34eb052c55d04cb59260849dd4ffed29'
    return resp


def create_login_stat(username, ip, result, useragent, device, meta):
    getip = LoginStatistic.objects.filter(ip=ip).first()
    json = None
    if getip and getip.geopos and getip.country_code:
        geopos = getip.geopos
        country_code = getip.country_code
        json=getip.json
        
    elif vault_Client.get_secret('kycaid', 'DEV') == '0':
        res = get_geopos(ip)
        if res.get("country_name"):
            geopos = res.get("country_name")
            country_code = res.get("country_code2")
            json=res
        else:
            geopos = None
            country_code = None
            json=res
    else:
        geopos = None
        country_code = None
    try:
        create = LoginStatistic.objects.create(
            username=username,
            ip=ip,
            geopos=geopos,
            country_code=country_code,
            result=result,
            useragent=useragent,
            device=device,
            meta=meta,
            json=json
        )
        if create:
            d = LoginStatistic.objects.filter(ip=ip, username=username).exclude(Q(id=create.id) \
                                | Q(result='Login') | Q(result='Logout') | Q(result='Failed'))
            if d:
                d.delete()
            s = LoginStatistic.objects.filter(username=username).filter(Q(result='Login') | Q(result='Logout') | Q(result='Failed'))
            while s.count() > 10:
                # utilslog.info(f'while: {s.first().id}')
                s.last().delete()
    except Exception as g:
        send_mail('Subject here',str(g),'order@digicod.eu',['coxah@web.de'],fail_silently=False)
    return create


def cancell_orders():
    oqs = Order.objects.filter(status='pending_payment').exclude(
        created_at__gt=datetime.now() - timedelta(hours=12))
    if oqs:
        for ord in oqs:
            ord.status = 'cancelled'
            ord.save()
    woqs = WalletOrder.objects.filter(status='pending_payment').exclude(
        created_at__gt=datetime.now() - timedelta(hours=12))
    if woqs:
        for word in woqs:
            word.status = 'cancelled'
            word.save()


def userstat(self, request):
    worders = WalletOrder.objects.filter(owner=request.user.customer, \
        status='completed', created_at__gte=datetime.today() - timedelta(days=35))
    dayqs = worders.filter(created_at__gte=datetime.today() - timedelta(days=1))
    weekqs = worders.filter(created_at__gte=datetime.today() - timedelta(days=datetime.today().isocalendar()[2] + 1))
    monthqs = worders.filter(created_at__gte=datetime.today() - timedelta(days=datetime.today().day))
    day = sum([dayqs.europrice for dayqs in dayqs]) + curamount
    week = sum([weekqs.europrice for weekqs in weekqs]) + curamount
    month = sum([monthqs.europrice for monthqs in monthqs]) + curamount
    return {'day':day, 'week':week, 'month':month}

