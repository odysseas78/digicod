from pprint import pprint
import json
import requests
import os, sys
from collections import OrderedDict
sys.path.insert(0, '/home/dcback')

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django

django.setup()
from eshop.models import Brand, Category, Product, ShopSetting, Jsonfile

from eshop.kinguin.order import api_key, testmod



def sgetprod(page):
    url = f'https://gateway{testmod}kinguin.net/esa/api/v1/products?page={page}&limit=100&regionId=3&name=gift card&tags=prepaid'
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    resp = requests.get(url, headers=headers)
    return resp.json()

# pprint(sgetprod(1))

def getbalance():
    url = f'https://gateway{testmod}kinguin.net/esa/api/v1/balance'
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    resp = requests.get(url, headers=headers)
    return resp.json()

# print(getbalance())

def getfirst():
    first = set()
    h=0
    while h < 9:
        h+=1
        res = sgetprod(h)
        for item in res.get('results'):
            arr = item.get('name').split(' ')
            if not arr[1][0].isdigit() and not arr[1][len(arr[1])-1].isdigit() and len(arr[1]) > 1:
                first.add(arr[0]+' '+arr[1])
            else:
                first.add(arr[0])
    return first

# brand = Brand.objects.filter(category__name='Region Free')
# brand.update(currencyes='EUR')
# for itm in getfirst():
#     obj, create = Brand.objects.get_or_create(
#         title=itm,
#         defaults={
#         'wsaler':'Kinguin',
#         # 'category':category,
#         'api_title':f'name={itm}',
#         'slug':itm.lower().replace(' ','-'),
#         'facevals':'10,15'}
#     )
#     obj.save()
#     if obj:
#         obj.category.add(catego)

def getprod(prodid=None):
    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': api_key
    }
    if prodid:
        prd = Product.objects.filter(brand__wsaler='Kinguin').filter(sku=prodid).first()
        if prd:
            brands = Brand.objects.filter(title=prd.brand.title)
        else:
            return None
    else:
        brands = Brand.objects.filter(wsaler='Kinguin')
    n = 0
    d = 0
    b = 0
    for item in brands:
        n+=1
        url = f'https://gateway{testmod}kinguin.net/esa/api/v1/products?{item.api_title}'
        resp = requests.get(url, headers=headers).json()
        if resp.get('item_count') and resp.get('item_count') > 0 and getbalance().get('balance') > 130:
            # print(f"1___{resp.get('results')[0].get('images').get('cover').get('url')}")
            d+=1
            if resp.get('results')[0].get('images') and resp.get('results')[0].get('images').get('cover'):
                prodimg = resp.get('results')[0].get('images').get('cover').get('url')
            if resp.get('results')[0].get('images') and resp.get('results')[0].get('images').get('screenshots')[0]:
                prodimg = resp.get('results')[0].get('images').get('screenshots')[0].get('url')
            item.in_stock = True
            item.active = True
            item.image=prodimg
            # item.slug=resp.get('results')[0].get('name').lower().replace(' ','-').replace(':','')
            item.wsaler='Kinguin'
            item.save()
            # facevalue = 0
            for itm in resp.get('results'):
                b+=1
                if itm.get('images') and itm.get('images').get('cover'):
                    prodimg = itm.get('images').get('cover').get('url')
                if itm.get('images') and itm.get('images').get('screenshots')[0]:
                    prodimg = itm.get('images').get('screenshots')[0].get('url')
                for cur in item.currencyes.split(','):
                    if cur in itm.get('name'):
                        currency = cur
                        break
                    else:
                        currency = ''
                for faceval in item.facevals.split(','):
                    if faceval in itm.get('name'):
                        facevalue = faceval
                        break
                    else:
                        facevalue = 0
                if itm.get('regionalLimitations'):
                    reg = itm.get('regionalLimitations').replace('Region Free', 'ww').replace('Region free', 'ww').replace('Europe', 'eu')
                else:
                    reg = 'ww'
                try:
                    product, create = Product.objects.get_or_create(
                        sku=itm.get('productId'),
                        defaults={
                        'brand':item,
                        'title':itm['name'],
                        'image':prodimg,
                        'price':0,
                        'profit':0,
                        'profit_fixed':0,
                        'pf_price':itm.get('price'),
                        'qty':itm.get('qty'),
                        'slug':itm.get('name').lower().replace(' ','-').replace(':',''),
                        'gtin':0,
                        'ean':0,
                        'region':reg,
                        'currency':currency,
                        'value':facevalue,
                        'active':True
                        }
                    )
                    if product:
                        
                        # product.brand=item
                        product.title=itm.get('name')
                        product.image=prodimg
                        product.pf_price=itm.get('price')
                        product.qty=itm.get('qty')
                        product.slug=itm.get('name').lower().replace(' ','-').replace(':','')
                        product.region=reg
                        product.currency=currency
                        product.value=facevalue
                        product.active=True
                        product.save()
                except:
                    pass
        else:
            # item.active = False
            item.in_stock = False
            item.save()
    
    

# getprod(prodid=None)