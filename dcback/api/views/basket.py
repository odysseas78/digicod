import os, json, pickle
from decimal import Decimal
from lib.PersistentDictObj import DictObj, PersistentDictObj



class BasketCls():
    
    
    def __init__(self):
        self.Dobj = DictObj
    
    
    
    def getdata(self, qty, vars):
        
        trash = vars.get('GetBasket').get('trash')
        addproduct = vars.get('GetBasket').get('addproduct')
        addcurrency = vars.get('GetBasket').get('addcurrency')
        addpayment = vars.get('GetBasket').get('addpayment')
        wallet = vars.get('GetBasket').get('wallet')
        data = {'trash':trash} if trash else {'id':addproduct, 'value':qty} if addproduct else \
            {'currency':addcurrency} if addcurrency else {'payment':addpayment} if addpayment else {'wallet':wallet}
    
        return data
    
    
    
    
    def sz(self, sz, basket):
        szdata = self.Dobj({**sz.data})
    
        limit = Decimal(szdata.limit)
        s = Decimal(round(limit - basket.total_price * basket.currency.price,2))
        # s = Decimal(round((limit + limit*Decimal(0.10)) - basket.total_price,2))
        szdata.limit = s
        return self.Dobj({'limit':limit, 's':s, 'szdata':szdata})
        





