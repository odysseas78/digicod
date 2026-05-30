import hashlib
import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
sys.path.append(str(BASE_DIR))
from collections import OrderedDict
from config.settings import vault_Client.get_secret
# from eshop.hc_vault.vault_client import vault_Client

import requests


def xml_parser(xmldata: str) -> dict:
    data = xmldata
    obj = {}
    data = data.replace(' xsi:type="xsd:string"', '').replace(' xsi:type="xsd:int"', '')
    data = re.findall("<[A-Za-z]{2,}>[A-Za-z0-9 -/:]{1,}</", data)
    for item in data:
        obj[item.replace('<', '').replace('/', '').split('>')[0]] = item.replace('<', '').replace('/', '').split('>')[1]
    return obj


def soap_get_trx_detail(trxid: str, test: str) -> dict:

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
    return xml_parser(response.text)


# print(soap_get_trx_detail('258cc2aa-d82f-42c1-bff3-a5a48d69fe40', 'no'))


def neosurf_reverse(trxid: int, currency: str, amount: float):
    # expiry = (datetime.now(timezone.utc) + timedelta(minutes=120)).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    amoun = int(float(round(amount, 2)) * 100)
    mtrxid = 'REVERSE'+str(trxid)
    order = {'amount': str(amoun), 'currency': currency, 'hash': "", 'merchantId': "24738",
             'merchantTransactionId': mtrxid, 'originalMerchantTransactionId': str(trxid),
             'subMerchantId': "digicod.eu", 'test': 'yes', "version": "3"
             }
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
                         <transactionNeosurfReverse xmlns="https://www.neosurf.info/soap/#transactionNeosurfReverse">
                         <transactionNeosurfReverseRequest>
                             <amount type="xsd:int">{str(amoun)}</amount>
                             <currency type="xsd:string">{currency}</currency>
                             <hash type="xsd:string">{hashk}</hash>
                             <merchantId type="xsd:int">24738</merchantId>
                             <merchantTransactionId type="xsd:string">{mtrxid}</merchantTransactionId>
                             <originalMerchantTransactionId type="xsd:string">{trxid}</originalMerchantTransactionId>
                             <subMerchantId type="xsd:string">digicod.eu</subMerchantId>
                             <test type="xsd:string">yes</test>
                             <version type="xsd:int">3</version>
                             </transactionNeosurfReverseRequest>
                         </transactionNeosurfReverse>
                       </soap:Body>
                    </soap:Envelope>"""
    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }
    # POST request
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text


# print(neosurf_reverse(526601, 'eur', 10))


def soap_get_voucher_detail() -> dict:
    order = {'hash': "", 'merchantId': "24738", 'test': 'yes', 'pincode': "26TG9PFP7V", "version": "3"}
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
                         <voucherGetDetails xmlns="https://www.neosurf.info/soap/#voucherGetDetails">
                            <voucherGetDetailsRequest>
                                <hash type="xsd:string">{hashk}</hash>
                                <IDMerchant type="xsd:int">24738</IDMerchant>
                                <test type="xsd:string">yes</test>
                                <version type="xsd:int">3</version>
                                <pincode type="xsd:string">26TG9PFP7V</pincode>
                            </voucherGetDetailsRequest>
                         </voucherGetDetails>
                       </soap:Body>
                    </soap:Envelope>"""
    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }
    # POST request
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text
    # return xml_parser(response.text)

# print(soap_get_voucher_detail())