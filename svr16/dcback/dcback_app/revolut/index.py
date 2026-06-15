import decimal
import pickle
import time, requests, json,sys, os
from datetime import datetime, timedelta
from pprint import pprint
from time import sleep
# sys.path.insert(0, '/home/dcback')
sys.path.insert(0, '/home/dcback')
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from eshop.models import Currency
from lib.PersistentDictObj import DictObj, PersistentDictObj


# ts = time.time() + timedelta(days=350).total_seconds()

# print(datetime.fromtimestamp(1747013841))
# print(time.time())    
# print(int(ts))

class Revolut(object):
    
    
    def __init__(self, db):
        self.db = db
        self.jwt = db.jwt
        self.code = db.code
        self.client_id = db.client_id
        self.access_token = db.access_token
        self.refresh_token = db.refresh_token
        self.expires_in = db.expires_in

    def check_token(self):
        tm = int(time.time())
        try:
            if tm >= (self.db.expires_in - 60):
                res = self.get_refresh_token()
                # print(res)
                self.db.access_token = res.get('access_token')
                self.db.expires_in = res.get('expires_in')+tm
                return True
            elif tm < self.db.expires_in:
                return True
            else:
                return {'res':res, 'res2':res}
        except Exception as e:
            return {'error': e}
        
    def get_token(self):
        payload = {
            "grant_type": "authorization_code",
            "code": self.code,
            "client_id": self.client_id,
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": self.jwt
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded--data',
        }

        resp = requests.post("https://b2b.revolut.com/api/1.0/auth/token", data=payload, headers=headers)
        try:
            return resp.json()
        except:
            return resp.text


    def get_refresh_token(self):
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": self.jwt
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded--data',
        }

        resp = requests.post("https://b2b.revolut.com/api/1.0/auth/token", data=payload, headers=headers)
        try:
            return resp.json()
        except:
            return resp.text


    def getCurrencyRates(self,cur1, cur2):
        chk = self.check_token()
        if chk != True:
            return chk
        payload = {}
        headers = {
        'Authorization': f'Bearer {self.access_token}',
        }
        url = f"https://b2b.revolut.com/api/1.0/rate?from={cur1}&amount=1&to={cur2}"
        resp = requests.get(url, headers=headers, data=payload)
        try:
            return resp.json()
        except:
            return resp.text




dbh = PersistentDictObj('/home/dcback/revolut/lib/db')

r = Revolut(dbh)

qs = Currency.objects.filter(active=True).exclude(shortname='EUR')
def updatecurrencyes():
   
    k = list()
    for i in qs:
        res = r.getCurrencyRates('EUR', i.shortname)
        i.orig_price = res.get('rate')
        i.save()
        k.append(res)
        sleep(2)
    r.db.currency = list(k)

if __name__ == '__main__':
    updatecurrencyes()
    r.db._save()
    print('done')

