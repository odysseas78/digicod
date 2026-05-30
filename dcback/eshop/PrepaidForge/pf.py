import sys, os, django, json, time
from typing import Any
from decimal import Decimal
from django.db.models import Q
from pprint import pprint
from dataclasses import dataclass



sys.path.insert(0, '/home/dcback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'


django.setup()
import requests
from config.settings import vault_Client.get_secret
# from lib.PersistentDictObj import PersistentDictObj

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)


from eshop.models import  Jsonfile, ShopSetting, Product, Brand, Category, ProductCodes, Orders
from eshop.PrepaidForge.functions import random_code
from lib.PersistentDictObj import PersistentDictObj

# shopsettings = PersistentDictObj(file_path='/home/dcback/shop/shopsettings', jsononly=True)

# db = PersistentDictObj(file_path='/home/dcback/eshop/PrepaidForge/db', jsononly=True)

# if not shopsettings.hasattr('testmode'): shopsettings.testmode = False
# if shopsettings.testmode == True:
#     PF_EMAIL = vault_Client.get_secret('pf/test', 'PF_TEST_EMAIL')
#     PF_PASSWORD = vault_Client.get_secret('pf/test', 'PF_TEST_PASSWORD')
# else:
#     PF_EMAIL = vault_Client.get_secret('pf/live', 'PF_EMAIL')
#     PF_PASSWORD = vault_Client.get_secret('pf/live', 'PF_PASSWORD')
# print(PF_EMAIL)

PF_EMAIL = vault_Client.get_secret('pf/test', 'PF_TEST_EMAIL')
PF_PASSWORD = vault_Client.get_secret('pf/test', 'PF_TEST_PASSWORD')
# PF_EMAIL = vault_Client.get_secret('pf/live', 'PF_EMAIL')
# PF_PASSWORD = vault_Client.get_secret('pf/live', 'PF_PASSWORD')

def json_read(file):
        if not os.path.exists(file):
            out_file = open(file, "w")
            json.dump({}, out_file, indent=2)
            out_file.close()
        with open(file, 'r') as file:
            try:
                return json.load(file)
            except Exception as d:
                return {}
@dataclass
class Pforge():
    all_prod_url = 'https://api.prepaidforge.com/v1/1.0/findAllProducts'
    def json_read(self, file):
        if not os.path.exists(file):
            out_file = open(file, "w")
            json.dump({}, out_file, indent=2)
            out_file.close()
        with open(file, 'r') as file:
            try:
                return json.load(file)
            except Exception as d:
                return {}

    def json_save(self, data, file):
        out_file = open(file, "w")
        json.dump(data, out_file, indent=2)
        out_file.close()
    
    
    def get_all_prod(self):
        url = self.all_prod_url
        headers = {'Content-Type': 'application/json'}
        resp = requests.get(url, headers=headers)
        try:
            ret = resp.json()
            return ret
        except:
            return resp.text
        
    
    def request(self, path, data):
        act_api_token = ShopSetting.objects.get(id=1)
        if act_api_token.pf_api_token_time < int(str(time.time())[:10]):
            url = 'https://api.prepaidforge.com/v1/1.0/signInWithApi'
            body = {
                "email": vault_Client.get_secret('pf/live', 'PF_EMAIL'),
                "password": vault_Client.get_secret('pf/live', 'PF_PASSWORD')
            }
            headers = {'Content-Type': 'application/json'}
            resp = requests.post(url, json=body, headers=headers).json()
            act_api_token.pf_api_token_time = int(str(resp['tokenValidUntil'])[:10])
            act_api_token.pf_api_token = resp['apiToken']
            # act_api_token.pf_test_mode = setting.get('Other').get('TestModus')
            act_api_token.save()
            act_api_token = ShopSetting.objects.get(id=1)

        # url = f'https://api.prepaidforge.com/v1/1.0/findStocks'
        url = f'https://api.prepaidforge.com/v1/1.0/{path}'
        headers = {'Content-Type': 'application/json',
                'X-PrepaidForge-Api-Token': act_api_token.pf_api_token}
        resp = requests.post(url, json=data, headers=headers).json()
        return resp

    def findStock(self, skus):
        data = {"types": ["TEXT", "SCAN"], "skus": [*skus]}
        return self.request('findStocks', data)

    def prorder(self, orderqs):
        
        products = orderqs.basket.products.all()
        basket_products =  orderqs.basket.basket_products

        s = list()
        for pr in products:
            s.append(pr.sku)
            s = set(s)
            s = list(s)
        stock = self.findStock(s)
        for pr in products:
            stck = [stk for stk in stock if stk.get('product') == pr.sku][0]
            if basket_products[f'{pr.id}'].get('qty') > stck.get('quantity'):
                self.setPrices()
                return {"type":"error","message":"low stock"}
        for pr in products:
            stck2 = [stk2 for stk2 in stock if stk2.get('product') == pr.sku][0]
            data = {"sku": pr.sku, "price": stck2.get('purchasePrice'), "codeType": stck2.get('type')}
            i = basket_products[f'{pr.id}'].get('qty')
            if basket_products[f'{pr.id}'].get('prcode'):
                continue
            while i > 0:
                rdcode = random_code(6, True, False, True, False)
                data['customOrderReference'] = f'{orderqs.uuid}-{rdcode}'
                resp = self.request('createApiOrder', data)
                print(resp)
                cr = ProductCodes.objects.create(
                        basket=orderqs.basket,
                        order=orderqs,
                        pf_order_id=resp.get('orderReference'),
                        orderid=resp.get('customOrderReference'),
                        code=resp.get('code'),
                        serial=resp.get('serial'),
                        downloadLink=resp.get('downloadLink'),
                        codeType=resp.get('codeType')
                    )
                cr.basket.basket_products[f'{pr.id}'].update({"prcode":cr.id})
                cr.basket.save()
                cr.order.products[f'{pr.id}'].update({"prcode":cr.id})
                cr.order.save()
                cr.save()
                i -= 1
        return {"type":"success", "message":"ok"}
        
    def create_brand(self, prdb, categ):
        brcreate = Brand.objects.create(
            # category=categories,
            wsaler='Prepaidforge',
            title=prdb.get('brand'),
            api_title=prdb.get('brand'),
            slug=prdb.get('brand').lower().replace("'", '').replace(' ', '_').replace('’', '').replace('-', '_'),
            image=prdb.get('imageUrl'),
            # image2 = models.ImageField(null=True, blank=True)
            imagepf=prdb.get('imageUrl'),
            # description = models.TextField(verbose_name='Description', null=True, blank=True, default=None)
            active=True,
            in_stock = True
            )
        brcreate.category.add(categ)
        brcreate.save()
        return brcreate

    def update_brand(self, bqs, categ, prdb):
        try:
            bqs.in_stock=True
            bqs.save()
            if not bqs.image:
                bqs.image = prdb.get('imageUrl')
                bqs.save()
            if not bqs.category.all():
                bqs.category.add(categ)
                bqs.save()
            return 'ok'
        except Exception as d:
            return d

    def create_product(self, bqs, prdb, quantity, value, purchasePrice, stock):
        prcreate = Product.objects.create(
            brand=bqs,
            title=prdb.get('name'),
            image=prdb.get('imageUrl'),
            # price=0,
            # profit=0,
            profit_fixed=0,
            pf_price=Decimal(purchasePrice),
            qty=quantity,
            sku=prdb.get('sku'),
            slug=prdb.get('sku').lower().replace("'", '').replace(' ', '_').replace('’', '').replace('-', '_'),
            gtin=prdb.get('gtin'),
            ean=prdb.get('ean'),
            region=prdb.get('countries')[0].lower(),
            currency=prdb.get('faceValue').get('currency'),
            value=value,
            active=True,
            in_stock=True,
            jsondata={'product':prdb, 'stock':stock, 'regions':prdb.get('countries')}
        )
        prcreate.save()
        return prcreate

    def update_product(self, prqs, prdb, purchasePrice, quantity, value, stock):
        prqs.update(
            title=prdb.get('name'), 
            pf_price=Decimal(purchasePrice), 
            qty=quantity, 
            gtin=prdb.get('gtin'), 
            ean=prdb.get('ean'), 
            region=prdb.get('countries')[0].lower(),
            currency = prdb.get('faceValue').get('currency'),
            value = value,
            jsondata = {'product':prdb, 'stock':stock, 'regions':prdb.get('countries')},
            in_stock = True,             
            )
        prqs.first().save()
        return prqs

    def facevalue_nomalize(self, prdb):
        valbrands = [
                'Free Fire', 'Runescape', 'FC25', 'Minecraft', 'Xbox Game Pass Ultimate', 'Nintendo', 'NCSOFT', 'Apex Legends Mobile', 'Mobile Legends', 'PUBG',
                'Spotify', 'ToneoFirst', 'Fortnite', 'Razer Gold', 'Azteco voucher lightning', 'Azteco voucher on chain'
                ]
        if prdb.get('brand') in valbrands:
            brnd = prdb.get('brand')
            if brnd == 'FC25':
                brnd = 'EA SPORTS FC 25'
            if brnd == 'ToneoFirst':
                brnd = 'Toneo First'
            if brnd == 'Razer Gold':
                brnd = 'Razer Gold'
            if brnd == 'Azteco voucher lightning':
                brnd = 'Azteco Bitcoin Lightning Voucher'
            if brnd == 'Azteco voucher on chain':
                brnd = 'Azteco Bitcoin On-Chain Voucher'
            value = prdb.get('name').replace('-', '').replace(brnd, '').strip()
            return value
        else:
            return None
    
    def db_refresh(self):
        self.json_save(self.get_all_prod(), '/home/dcback/eshop/PrepaidForge/db.json')
        self.db = self.json_read('/home/dcback/eshop/PrepaidForge/db.json')
        s = list()
        for pr in self.db:
            s.append(pr.get('sku'))
            s = set(s)
            s = list(s)
        self.json_save(self.findStock(s), '/home/dcback/eshop/PrepaidForge/db2.json')
        self.db2 = self.json_read('/home/dcback/eshop/PrepaidForge/db2.json')

    def setPrices(self):
        
        brandqs = Brand.objects.filter(wsaler='Prepaidforge')
        catqs = Category.objects.all()
        self.db_refresh()
        for prdb in self.db:
            prdb_sku = prdb.get('sku')
            filtred = [prdb2 for prdb2 in self.db2 if prdb2.get("product") == prdb_sku]
            if not filtred: continue
            stock = filtred
            quantity = sum([product.get('quantity') for product in stock])
            purchasePrice = max([product.get('purchasePrice') for product in stock])

            bqs = brandqs.filter(title=prdb.get('brand')).first()
            categ = catqs.filter(pf_name=prdb.get('category')[0]).first()
            # value = f"{prdb.get('faceValue').get('amount')} {prdb.get('faceValue').get('currency')}"
            value = prdb.get('name').replace('-', '').replace(prdb.get('brand'), '').strip()
            #############################################
            valueres = self.facevalue_nomalize(prdb)
            if valueres:
                value = valueres
            #############################################
            if not bqs:
                bqs = self.create_brand(prdb, categ)
                if bqs: print("new Brand add: "+prdb.get('brand'))

            elif bqs and (not bqs.in_stock or not bqs.image or not bqs.category.all()):
                res = self.update_brand(bqs, categ, prdb)
                if res != 'ok': pprint(res)
            prqs = bqs.products.filter(sku=prdb_sku)
            if not prqs:
                prcreate = self.create_product(bqs, prdb, quantity, value, purchasePrice, stock)
                if prcreate: print("new product add: "+prdb_sku)
            elif prqs:
                self.update_product(prqs, prdb, purchasePrice, quantity, value, stock)
        # check Out of stock ########################
        prodqs = Product.objects.filter(brand__wsaler='Prepaidforge')
        prodqs2 = prodqs.filter(qty__gt=0, in_stock=True)
        for prod in prodqs2:
            a2 = prod.sku
            filtred = [product for product in self.db2 if product.get("product") == a2]
            if not filtred:
                prod.qty = 0
                prod.save()
                print(f'Out of stock - {prod.title}')



# pf = Pforge()
# pf.setPrices()
# pf.db_refresh()
# brands = list()
# lst = list()
# db = json_read('/home/dcback/eshop/PrepaidForge/db.json')
# db2 = json_read('/home/dcback/eshop/PrepaidForge/db2.json')
# for it in db2:
#     filtred = [prdb for prdb in db if prdb.get("sku") == it.get('product')]
#     title = filtred[0].get('brand')
#     category = filtred[0].get('category')[0]
#     if category == 'Mobile':
#         category = 'Mobile Recharge'
#     if title not in brands:
#         lst.append({"title":title, "category": category})
#         brands.append(title)

# lst = list(set(lst))
# pprint(lst)
# pf.json_save(lst,'/home/dcback/eshop/PrepaidForge/titledb.json')
# print(len(lst))

# Output: '3'
# orderqs = Orders.objects.filter(id=10).first()
# pf.prorder(orderqs)
# products = orderqs.basket.products
# print(products.all())
# f = ['id', 'brand', 'title', 'image', 'price', 'in_stock', 'profit', 'profit_fixed', 'pf_price', 'qty', 'sku', 'slug', 'gtin', 'ean', 'region', 'currency', 'value', 'active', 'description', 'jsondata', 'deleted', 'created_at', 'updated_at']


# for prdb in db:
#     prdb_sku = prdb.get('sku')
#     filtred = [prdb2 for prdb2 in db2 if prdb2.get("product") == prdb_sku]
#     if not filtred: continue
#     stock = filtred
#     quantity = sum([product.get('quantity') for product in stock])
#     purchasePrice = max([product.get('purchasePrice') for product in stock])
#     print(purchasePrice)
#     pprint(quantity)
#     pprint(stock)
#     print('###############################################')
# pqs = Product.objects.filter(brand__wsaler='Prepaidforge', id=6714).first()
# jsn = Jsonfile.objects.filter(name='Shopsettings').first()
# # # print([field.name for field in Product._meta.fields])
# pqs.update(description='')
# pqs.jsondata.update({"holisterini":'aaaaaaaaaaaaaaaaaaaaaaaaaaaa'})
# print(jsn.json)
# brandqs = Brand.objects.filter(wsaler='Prepaidforge')
# prodqs2 = brandqs.first().products.filter(qty__gt=12000)
# print(prodqs2)
# for prod2 in prodqs2.all():
#     print(prod2.sku)
#     break
#     filtred = [product for product in db2 if product.get("product") == sku]
#     if not filtred:
#         prod2.active = False
#         prod2.qty = 0
#         prod2.in_stock = False
#         prod2.save()
#         print(f'Out of stock - {prod2.title}')

# al = list()
# for prod in prodqs:
#     print(f'{prod.value} - {prod.title} - {prod.brand.title}')
    # sl = prod.value.split('.')
#     sl2 = sl[1] if len(sl) > 1 else sl[0]
#     # print(f'{sl} - {prod.value}')
#     sl3 = sl2.split(' ')
#     # print(f'{sl3} - {len(sl3)}')
#     if sl3[0] != '0':
#         al.append(prod.brand.title)
# al = list(set(al))
# print(f'{al}')
    # if slist[1] != '0':
    #     print(f'{prod.title} - {prod.value}')

# def set_img():
    # imgcount = 0
    # brandcount = 0
    # imgs = os.scandir('C:/Users/omart/Google Drive/PycharmProjects/digicod_rest_api/media/brands')
    # brands = Brand.objects.exclude(image2='')
    # for img in imgs:
    #     imgcount += 1
    #     # print(f' - {img.name[:-4]}')
    #     for brand in brands:
    #         if brand.slug == img.name[:-4].split("-")[0]:
    #             brandcount += 1
    #             print(f'{brand.slug} - {img.name.split("-")[0]}')
    #             # brand.image2 = f'/brands/{img.name}'
    #             # brand.save()
    # print(f'{imgcount} - {brandcount}')
    # print(brands.count())


# set_img()
# print(sys.path)

# def check_images():
    # brands = Brand.objects.all()
    # for brand in brands:
    #     if not brand.image:
    #         print(brand.title)


# check_images()

# def reset_profit():
    # products = Product.objects.all()
    # for product in products:
    #     product.profit = 0
    #     product.profit_fixed = 0
    #     product.save()

# reset_profit()


# print(time.time())
# print(int(str(time.time())[:10]))
# print(int(str(resp['tokenValidUntil'])[:10]))
# print(int(str(time.time())[:10]) - int(str(resp['tokenValidUntil'])[:10]))
# print(int(str(resp['tokenValidUntil'])[:10]) - int(str(time.time())[:10]))
# print('--------------------')
# api_token = resp['apiToken']
