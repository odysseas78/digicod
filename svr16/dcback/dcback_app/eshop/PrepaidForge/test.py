import sys, os, django, json
from django.db.models import Q
from pprint import pprint
import time
import requests
from pathlib import Path
sys.path.insert(0, '/home/dcback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
# from PF import *
# from Order import *
# from eshop.Utilss.utils import DictObj
from eshop.models import Category, Product, Brand, ShopSetting
from config.settings import vault_Client.get_secret
from decimal import Decimal

# VAULT_URL = 'http://10.251.167.111:8888'
# VAULT_ROLE_ID = '12f52ac3-2c4a-8b51-ad6b-7404a068f3bd'
# VAULT_SECRET_ID = 'cff50237-223b-0992-9b1f-05513c3f613f'

# VAULT_TOKEN = None  # Wird zur Laufzeit gesetzt
# from eshop.hc_vault.vault_client import vault_Client
# env_dict = vault_Client.get_secret('data','dcdev', 'kv')
# BASE_DIR = Path(__file__).resolve().parent.parent

# def vault_Client.get_secret(pathkey, key):
#     return vault_Client.get_secret('data', pathkey, 'kv').get(key)

# PF_EMAIL = vault_Client.get_secret('pf/live', 'PF_EMAIL')
# PF_PASSWORD = vault_Client.get_secret('pf/live', 'PF_PASSWORD')





    
    
# def jaccard_similarity(str1, str2):
#     l1, l2 = str1.replace(' ','').replace('-','').lower(), str2.replace(' ','').replace('-','').lower()
#     res = ((l1[0:len(l2)] == l2)  and (abs(len(l1) - len(l2)) < 2)) if (len(l1) > len(l2)) else ((l2[0:len(l1)] == l1) and (abs(len(l1) - len(l2)) < 2))
#     return res



class Pforge():
    
    def __init__(self):
        pass
   
    
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
        url = 'https://api.prepaidforge.com/v1/1.0/findAllProducts'
        headers = {'Content-Type': 'application/json'}
        resp = requests.get(url, headers=headers)
        try:
            ret = resp.json()
            return ret
        except:
            return resp.text
        
    
    def findStock(self, skus):
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

        url = 'https://api.prepaidforge.com/v1/1.0/findStocks'
        headers = {'Content-Type': 'application/json',
                'X-PrepaidForge-Api-Token': act_api_token.pf_api_token}
        data = {"types": ["TEXT", "SCAN"], "skus": [*skus]}

        resp = requests.post(url, json=data, headers=headers).json()
        return resp
        
        
    def setPrices(self):
        prodqs = Product.objects.filter(brand__wsaler='Prepaidforge')
        brandqs = Brand.objects.filter(wsaler='Prepaidforge')
        self.json_save(self.get_all_prod(), '/home/dcback/eshop/PrepaidForge/db.json')
        self.db = self.json_read('/home/dcback/eshop/PrepaidForge/db.json')
        s = list()
        for pr in self.db:
            s.append(pr.get('sku'))
            s = set(s)
            s = list(s)
        self.json_save(self.findStock(s), '/home/dcback/eshop/PrepaidForge/db2.json')
        self.db2 = self.json_read('/home/dcback/eshop/PrepaidForge/db2.json')
        
        for pr2 in self.db2:
            a = pr2.get('product')
            filtred = [product for product in self.db if product.get("sku") == a]
            b = filtred[0]
            value = f"{b.get('faceValue').get('amount')} {b.get('faceValue').get('currency')}"
            
            #############################################
            valbrands = [
                'Free Fire', 'Runescape', 'FC25', 'Minecraft', 'Xbox Game Pass Ultimate', 'Nintendo', 
                'NCSOFT', 'Apex Legends Mobile', 'Mobile Legends'
                ]
            if b.get('brand') in valbrands:
                brnd = b.get('brand')
                if brnd == 'FC25':
                    brnd = 'EA SPORTS FC 25'
                # print(b.get('name'))
                value = b.get('name').replace('-', '').replace(brnd, '').strip()
            #############################################
            pqs = prodqs.filter(sku=a).first()
            if pqs:
                bqs = brandqs.filter(title=b.get('brand')).first()
                if not bqs:
                    print("brand error")
                # pqs.brand = bqs
                pqs.title = b.get('name')
                # pqs.image = img
                pqs.pf_price = Decimal(pr2.get('purchasePrice'))
                pqs.qty = pr2.get('quantity')
                # pqs.sku=item['sku']
                # pqs.slug=item['sku']
                pqs.gtin = b.get('gtin')
                pqs.ean = b.get('ean')
                pqs.region = b.get('countries')[0].lower()
                pqs.currency = b.get('faceValue').get('currency')
                pqs.value = value
                pqs.jsondata = {'product':b, 'stock':pr2}
                pqs.active = True
                pqs.in_stock = True
                pqs.description = ''
                pqs.save()
                pqs.brand.active = True
                pqs.brand.in_stock = True
                pqs.brand.description = ''
                pqs.brand.save()
                if not pqs.brand.image:
                    for pr in self.db:
                        if pr.get('sku') == a:
                            pqs.brand.image = pr.get('imageUrl')
                            pqs.brand.save()
                            break
            else:
                print("new product: "+a)
                bqs = brandqs.filter(title=b.get('brand')).first()
                if not bqs:
                    create = Brand.objects.create(
                    # category=categories,
                    wsaler='Prepaidforge',
                    title=b.get('brand'),
                    api_title=b.get('brand'),
                    slug=b.get('brand').lower().replace("'", '').replace(' ', '_').replace('’', '').replace('-', '_'),
                    image=b.get('imageUrl'),
                    # image2 = models.ImageField(null=True, blank=True)
                    imagepf=b.get('imageUrl'),
                    # description = models.TextField(verbose_name='Description', null=True, blank=True, default=None)
                    active=True,
                    in_stock = True
                    )
                    categ = Category.objects.filter(pf_name=b.get('category')[0]).first()
                    create.category.add(categ)
                    create.save()
                bqs2 = brandqs.filter(title=b.get('brand')).first()
                create2 = Product.objects.create(
                brand=bqs2,
                title=b.get('name'),
                image=b.get('imageUrl'),
                # price=0,
                # profit=0,
                profit_fixed=0,
                pf_price=Decimal(pr2.get('purchasePrice')),
                qty=pr2.get('quantity'),
                sku=b.get('sku'),
                slug=b.get('sku').lower().replace("'", '').replace(' ', '_').replace('’', '').replace('-', '_'),
                gtin=b.get('gtin'),
                ean=b.get('ean'),
                region=b.get('countries')[0].lower(),
                currency=b.get('faceValue').get('currency'),
                value=value,
                active=True,
                in_stock=True,
                jsondata={'product':b, 'stock':pr2}
                )
                create2.save()





# cat = ['GiftCard','Mobile','PaymenCard']
# bqs = Brand.objects.filter(title='Xbox Live').first()
# categ = Category.objects.filter(pf_name=cat[1]).first()
# # bqs.category.add(categ)




# db = pf.json_read('/home/dcback/eshop/PrepaidForge/db.json')
# filtred = [product for product in db if product.get("sku") == 'EA-SPORTS-FC-25-1050-FC-POINTS']
# print(filtred)
# pf.findStock()


# print(len(res))
# resp = get_all_prod()
# json_save(resp, './db.json')

# response = requests.get("https://despv2wf92pf4.cloudfront.net/961519fe-5e7e-46cc-8c26-8e670fdda89d.png")
# file = open("/home/dcback/eshop/PrepaidForge/sample_image.png", "wb")
# file.write(response.content)
# rescont = {
#     "filecontent": response.content
# }
# file.close()




    

                
# f1()

# get and save al pf producte
# 

class PfProducts(object):

    def getDatatoDB(self):
        allproducts = get_all_prod()

    def normalizeSavedpfdata(self, data):
        r = []
        cat = []
        for i in data.copy():
            r.append(i.to_dict())
            cat.append(*i.to_dict().get("category"))
        self.pfcategories = list(set(cat))
        self.pfdata = [p for p in r if (p.get("active") == True and 'Games' not in p.get('category'))]
        return list(set(cat))

    def checkcategories(self):
        categ = Category.objects.all()
        categories = [p.pf_name for p in categ]
        categoriescompare = [c for c in self.pfcategories if c not in categories]
        return categoriescompare
    
    def getOrCreateCategory(self):
        c = self.checkcategories()
        if len(c) > 0:
            for cat in c:
                create = Category.objects.create(pf_name=cat, name=cat, active=False, slug=cat.lower().replace(' ', '_'))
            return create

    def createBrand(self, item, img, categories):
        create = Brand.objects.create(
        # category=categories,
        wsaler='Prepaidforge',
        title=item.get('brand') if item.get('brand') else item.get('name') if item.get('name') else 'ERROR',
        api_title=item.get('brand') if item.get('brand') else item.get('name') if item.get('name') else 'ERROR',
        slug=item.get('brand').lower().replace(' ', '_') if item.get('brand') else item.get('name').lower().replace(' ', '_'),
        image=img,
        # image2 = models.ImageField(null=True, blank=True)
        imagepf=item['imageUrl'],
        # description = models.TextField(verbose_name='Description', null=True, blank=True, default=None)
        active=True
        )
        categ = Category.objects.filter(pf_name=categories[0]).first()
        create.category.set(categ)
        create.save()
        # create.category.set(categ)
        return create
    
    def createProduct(self, item, img, brand):
        create = Product.objects.create(
        brand=brand,
        title=item['name'],
        image=img,
        price=0,
        profit=0,
        profit_fixed=0,
        pf_price=0,
        qty=0,
        sku=item['sku'],
        slug=item['sku'],
        gtin=0,
        ean=0,
        region=item['countries'][0],
        currency=item['faceValue']['currency'],
        value=item['faceValue']['amount'],
        active=True,
        jsondata=item
        )
        create.save()
        return create
    
    def getImages(self,item):
        img = '/'
        try:
            imgurl = item['imageUrl']
            response = requests.get(imgurl)
            with open(
                f"/home/dcui/public/media/prodimg/{item['brand'].lower().replace(' ', '_')}.png", "wb") as file:
                file.write(response.content)
                file.close()
            img = f"/prodimg/{item['brand'].lower().replace(' ', '_')}.png"
        except Exception as d:
            print(d)
        return img
    

    def getOrCreateProduct(self, data):
        pr = Product.objects.filter(brand__wsaler='Prepaidforge')
        # if not self.pfdata: self.normalizeSavedpfdata(self)
        for item in data:
            prod = pr.filter(Q(sku=item.get('sku')) | Q(title=item.get('name')) | Q(slug=item.get('sku'))).first()
            if not prod:
                brand = Brand.objects.filter(title=item.get('brand')).first()
                if not brand:
                    # image = self.getImages(item)
                    creabrand = self.createBrand(item, '', item.get('category'))
                # image = self.getImages(item)
                brand = creabrand
                self.createProduct(item, '', brand)
            else:
                prod.region = item.get('countries')[0]
                prod.jsondata = item
                prod.save()
        return 'Done'
    

# resp = json_read('/home/dcback/eshop/PrepaidForge/db.json')
# cl = PfProducts()
# # cl.getDatatoDB()
# a = cl.normalizeSavedpfdata()
# print('aaaa',a)
# b = cl.getOrCreateCategory()
# print('bbbb',b)
# c = cl.getOrCreateProduct(resp)
# pr = Product.objects.filter(brand__wsaler='Prepaidforge')
# print(json.loads(pr.first().region))




# print(arraycompare(list1, list2))

# Ergebnis anzeigen
# for pair in similar_pairs:
#     print(f"{pair[0]} ≈ {pair[1]} ({pair[2]}%)")



# pr.delete()
# qs = Brand.objects.filter(wsaler='Prepaidforge')
# pr.delete()
# resp = f2()
# d = set()
# for i in qs:
#     if not pr.filter(brand=i):
#         print(pr.filter(brand=i))
        # i.delete()
#         d.add(i.get('brand'))
#         sku+=1
# print(pr.count())
# # print(notsku)

# print(pr.count())