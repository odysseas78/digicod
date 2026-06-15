import hashlib
import os
import json
import re
from collections import OrderedDict
from datetime import datetime, timezone, timedelta
import time
from loguru import logger
from django.core.mail import send_mail
# from django.db.models import Q
from config.settings import vault_Client.get_secret
# from rest_framework.response import Response
import requests

class Neosurf1(object):


    def neosurf_pay_send(self, orderqs, id, amount, currency, test, urlOk, urlKo, urlPending, urlCallback):
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
        orderqs.postdata = order
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
            if url: 
                orderqs.responsedata.update({"type": "success", "message": url})
                orderqs.save()
            return {"type": "success", "message": url}
        except:
            return {"type": "error", "message": 'There has been an error. Try again later or contact support. (NSF)'}

    def xml_parser(self, xmldata: str) -> dict:
        data = xmldata
        obj = {}
        data = data.replace(' xsi:type="xsd:string"', '').replace(' xsi:type="xsd:int"', '')
        data = re.findall("<[A-Za-z]{2,}>[A-Za-z0-9 -/:]{1,}</", data)
        for item in data:
            obj[item.replace('<', '').replace('/', '').split('>')[0]] = item.replace('<', '').replace('/', '').split('>')[1]
        return obj


    def soap_get_trx_detail(self, trxid: str, test: str) -> dict:

        if test == test:
            trxid = 'T'+str(trxid)

        order = {'hash': "", 'merchantId': "24738", 'merchantTransactionId': str(trxid), 'test': test, 'subMerchantId': "digicod.eu", "version": "3"}
        order = OrderedDict(sorted(order.items()))
        ordstr = ''.join(order.values()) + vault_Client.get_secret('neosurf', 'NEOSURF_SECRET')
        h = ordstr.encode()
        hashk = hashlib.sha512(h).hexdigest()
        order["hash"] = hashk

        # SOAP request URL
        url = "https://www.neosurf.info:443/soap/index.php"

        payload = f"""<?xml version="1.0"?>
                        <soap:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" 
                        xmlns:tns="https://www.neosurf.info/soap/"
                        targetNamespace="https://www.neosurf.info/soap/">
                        <soap:Body>
                            <transactionGetDetails xmlns="https://www.neosurf.info/soap/#transactionGetDetails">
                            <transactionGetDetailsRequest>
                                <hash type="xsd:string">{hashk}</hash>
                                <merchantId type="xsd:int">24738</merchantId>
                                <merchantTransactionId type="xsd:string">{trxid}</merchantTransactionId>
                                <subMerchantId type="xsd:string">digicod.eu</subMerchantId>
                                <test type="xsd:string">{test}</test>
                                <version type="xsd:int">3</version>
                                </transactionGetDetailsRequest>
                            </transactionGetDetails>
                        </soap:Body>
                        </soap:Envelope>"""
        headers = {
            'Content-Type': 'text/xml; charset=utf-8'
        }
        # POST request
        response = requests.request("POST", url, headers=headers, data=payload)
        return self.xml_parser(response.text)



class Neosurf(Neosurf1):

    def gg(self):
        pass


# result = neosurf_pay_send(id='test56h67878a', amount=3.56, currency='eur',
#                                                 test='yes',
#                                         urlOk="https://digicod.eu/payments/test56h67878a",
#                                         urlKo=f"https://digicod.eu/cancel/test56h67878a",
#                                         urlPending='https://digicod.eu/',
#                                         urlCallback="https://digicod.eu/callbck/test56h67878a")

# print(result)
