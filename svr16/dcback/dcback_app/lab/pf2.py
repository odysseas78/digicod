# from datetime import datetime, timedelta
# import json
# import os
# import sys
# import time


# # import socket
# # import socks
# # ip='127.0.0.10' # change your proxy's ip
# # port = 6000 # change your proxy's port
# # socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
# # socket.socket = socks.socksocket
# from django.conf import settings
# import django
# os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
# django.setup()
# from eshop.models import Jsonfile, Order
# import requests
# from config.settings import vault_Client.get_secret
# setting = Jsonfile.objects.filter(name='Shopsettings').first().json



# from eshop.models import Brand, Category, Product, ShopSetting

# if setting.get('Other').get('TestModus') == True:
#     PF_EMAIL = vault_Client.get_secret('pf/test', 'PF_TEST_EMAIL')
#     PF_PASSWORD = vault_Client.get_secret('pf/test', 'PF_TEST_PASSWORD')
# else:
#     PF_EMAIL = vault_Client.get_secret('pf/live', 'PF_EMAIL')
#     PF_PASSWORD = vault_Client.get_secret('pf/live', 'PF_PASSWORD')

# def do_private_query(self, requestMethod, requestUri, body=None):
#     requestUri = '/{0}'.format(requestUri)
#     url = '{0}{1}'.format(self.rootPath, requestUri)
#     mt = self.microtime().split(' ')
#     nonce = '{0}{1}'.format(mt[1], mt[0][2:6])

#     thejson = None
#     if body:
#         thejson = json.dumps(body, separators=(',', ':'))

#     headers = {'Content-Type': 'application/json'}
#     if requestMethod == 'PUT':
#         return requests.put(url, data=thejson, headers=headers)
#     elif requestMethod == 'POST':
#         return requests.post(url, data=thejson, headers=headers)
#     elif requestMethod == 'GET':
#         return requests.get(url, headers=headers)


# def get_all_products():
#     url = 'https://api.prepaidforge.com/v1/1.0/findAllProducts'
#     body = {
#         "email": PF_EMAIL,
#         "password": PF_PASSWORD
#     }
#     thejson = json.dumps(body, separators=(',', ':'))

#     headers = {'Content-Type': 'application/json'}

#     resp = requests.get(url, headers=headers).json()

#     # for item in resp:
#     #     if item['brand'][:4] == 'Amer':
#     #         print(item['category'][0])

#     for item in resp:
#         if item['category'][0] != 'Games':
#             brands = Brand.objects.filter(api_title=item['brand']).first()
#             # for cat in item['category']:
#             #     qs = Category.objects.filter(pf_name=cat).first()
#             #     brands.category.add(qs)
#             #     brands.save()
#             categories = Category.objects.filter(pf_name=item['category'][0]).first()
#             if not categories:
#                 categories = Category.objects.create(
#                     name=item['category'][0],
#                     slug=item['category'][0].lower().replace(' ', '_'),
#                     pf_name=item['category'][0],
#                 )
#             img = None
#             imgurl = None
#             if not brands:
#                 try:
#                     imgurl = item['imageUrl']
#                     response = requests.get(imgurl)
#                     file = open(
#                         f"/home/dcback/media/prodimg/{item['brand'].lower().replace(' ', '_')}.png", "wb")
#                     file.write(response.content)
#                     file.close()
#                     img = f"/prodimg/{item['brand'].lower().replace(' ', '_')}.png"
#                 except Exception as d:
#                     print(d)
#                 brands = Brand.objects.create(
#                     # category=category.set(),
#                     title=item['brand'],
#                     api_title=item['brand'],
#                     slug=item['brand'].lower().replace(' ', '_'),
#                     image=img,
#                     # image2 = models.ImageField(null=True, blank=True)
#                     imagepf=imgurl,
#                     # description = models.TextField(verbose_name='Description', null=True, blank=True, default=None)
#                     active=True
#                 )
#                 for cat in item['category']:
#                     qs = Category.objects.filter(pf_name=cat).first()
#                     brands.category.add(qs)
#                     brands.save()
#             check = Product.objects.filter(sku=item['sku']).first()
#             if not check:
#                 Product.objects.create(
#                     brand=brands,
#                     title=item['name'],
#                     image=img,
#                     price=0,
#                     profit=0,
#                     profit_fixed=0,
#                     pf_price=0,
#                     qty=0,
#                     sku=item['sku'],
#                     slug=item['sku'],
#                     gtin=0,
#                     ean=0,
#                     region=item['countries'][0],
#                     currency=item['faceValue']['currency'],
#                     value=item['faceValue']['amount'],
#                     active=True
#                 )


# # response = requests.get("https://despv2wf92pf4.cloudfront.net/961519fe-5e7e-46cc-8c26-8e670fdda89d.png")
# # file = open("../../media/prodimg/sample_image.png", "wb")
# # file.write(response.content)
# # file.close()
# # print(file)

# # get_all_products()

# #

# def set_prices():
#     # brands = Brand.objects.all()
#     products = Product.objects.all()
#     act_api_token = ShopSetting.objects.get(id=1)
#     if act_api_token.pf_api_token_time < int(str(time.time())[:10]) or act_api_token.pf_test_mode != setting.get('Other').get('TestModus'):
#         url = 'https://api.prepaidforge.com/v1/1.0/signInWithApi'
#         body = {
#             "email": PF_EMAIL,
#             "password": PF_PASSWORD
#         }
#         headers = {'Content-Type': 'application/json'}
#         resp = requests.post(url, json=body, headers=headers).json()
#         act_api_token.pf_api_token_time = int(str(resp['tokenValidUntil'])[:10])
#         act_api_token.pf_api_token = resp['apiToken']
#         act_api_token.pf_test_mode = settings.get('Other').get('TestModus')
#         act_api_token.save()
#         act_api_token = ShopSetting.objects.get(id=1)

#     url = 'https://api.prepaidforge.com/v1/1.0/findStocks'
#     headers = {'Content-Type': 'application/json',
#                'X-PrepaidForge-Api-Token': act_api_token.pf_api_token}
#     data = {"types": ["TEXT"], "skus": []}
#     for product in products:
#         data['skus'].append(product.sku)

#     resp = requests.post(url, json=data, headers=headers).json()
#     # print(data)
#     for product in products:
#         product.qty = 0
#         product.save()
#         for item in resp:
#             if item['product'] == product.sku:
#                 product.pf_price = item['purchasePrice']
#                 brand = Brand.objects.filter(id=product.brand.id).first()
#                 if item['purchasePrice'] > 0 and brand.active is False:
#                     brand.active = True
#                     brand.save()
#                 if item['quantity'] < 0:
#                     item['quantity'] = 88888888
#                 product.qty = item['quantity']
#                 product.save()
#                 if item['purchasePrice'] > 0:
#                     if not product.active:
#                         product.active = True
#                         product.save()
#                 elif product.active:
#                     product.active = False
#                     product.save()


# # set_prices()


# def find_stocks():
#     # brands = Brand.objects.all()
#     # products = Product.objects.all()
#     act_api_token = ShopSetting.objects.get(id=1)
#     if act_api_token.pf_api_token_time < int(str(time.time())[:10]) or act_api_token.pf_test_mode != setting.get('Other').get('TestModus'):
#         url = 'https://api.prepaidforge.com/v1/1.0/signInWithApi'
#         body = {
#             "email": PF_EMAIL,
#             "password": PF_PASSWORD
#         }
#         headers = {'Content-Type': 'application/json'}
#         resp = requests.post(url, json=body, headers=headers).json()
#         act_api_token.pf_api_token_time = int(str(resp['tokenValidUntil'])[:10])
#         act_api_token.pf_api_token = resp['apiToken']
#         act_api_token.pf_test_mode = setting.get('Other').get('TestModus')
#         act_api_token.save()
#         act_api_token = ShopSetting.objects.get(id=1)

#     url = 'https://api.prepaidforge.com/v1/1.0/findStocks'
#     headers = {'Content-Type': 'application/json',
#                'X-PrepaidForge-Api-Token': act_api_token.pf_api_token}
#     data = {"types": ["TEXT", "SCAN"], "skus": ['Steam-50-USD']}
#     # for product in products:
#     #     data['skus'].append(product.sku)

#     return requests.post(url, json=data, headers=headers).json()


# print(find_stocks())


# # curr = Currency.objects.create(
# #     longname='Euro',
# #     shortname='EUR',
# #     sign='€',
# #     image='flag-round-250.png',
# #     price=1.00
# #     )

# def set_img():
#     imgcount = 0
#     brandcount = 0
#     imgs = os.scandir('C:/Users/omart/Google Drive/PycharmProjects/digicod_rest_api/media/brands')
#     brands = Brand.objects.exclude(image2='')
#     for img in imgs:
#         imgcount += 1
#         # print(f' - {img.name[:-4]}')
#         for brand in brands:
#             if brand.slug == img.name[:-4].split("-")[0]:
#                 brandcount += 1
#                 print(f'{brand.slug} - {img.name.split("-")[0]}')
#                 # brand.image2 = f'/brands/{img.name}'
#                 # brand.save()
#     print(f'{imgcount} - {brandcount}')
#     print(brands.count())


# # set_img()
# # print(sys.path)

# def check_images():
#     brands = Brand.objects.all()
#     for brand in brands:
#         if not brand.image:
#             print(brand.title)


# # check_images()

# def reset_profit():
#     products = Product.objects.all()
#     for product in products:
#         product.profit = 0
#         product.profit_fixed = 0
#         product.save()


# def get_orders(start, end, page):
#     act_api_token = ShopSetting.objects.get(id=1)
#     if act_api_token.pf_api_token_time < int(str(time.time())[:10]) or act_api_token.pf_test_mode != setting.get('Other').get('TestModus'):
#         url = 'https://api.prepaidforge.com/v1/1.0/signInWithApi'
#         body = {
#             "email": 'admin@digicod.eu',
#             "password": 'jEz3xfidZi3SccC'
#         }
#         headers = {'Content-Type': 'application/json'}
#         resp = requests.post(url, json=body, headers=headers).json()
#         act_api_token.pf_api_token_time = int(str(resp['tokenValidUntil'])[:10])
#         act_api_token.pf_api_token = resp['apiToken']
#         act_api_token.pf_test_mode = setting.get('Other').get('TestModus')
#         act_api_token.save()
#         act_api_token = ShopSetting.objects.get(id=1)

#     url = f'https://api.prepaidforge.com/v1/1.0/getApiOrders'
#     headers = {'Content-Type': 'application/json',
#                'X-PrepaidForge-Api-Token': act_api_token.pf_api_token}
#     body = {
#             "page": page,
#             "startDate": start ,
#             "endDate": end
#             }

#     return requests.post(url, data=json.dumps(body), headers=headers)

# # order = Order.objects.filter(id=862992).first()
# # start = int(1000 * (order.created_at - timedelta(minutes=5)).timestamp())
# # end = int(1000 * (order.created_at + timedelta(days=1)).timestamp())

# # # start = int(1000 * (datetime.now() - timedelta(days=1)).timestamp())
# # # end = int(1000 * (datetime.now() + timedelta(days=1)).timestamp())
# # # print(get_orders(start=start, end=end, page=7).json())

# # page = 1
# # while True:
# #     result = get_orders(start, end, page).json()
    
# #     for item in result.get('content'):
# #         if int(item.get('customOrderReference')[:6]) == order.id:
# #             print(item)
# #     if result.get('pageCount') < 2:
# #         break
    
# #     page += 1
# #     if page == result.get('pageCount'):
# #         break
# #     time.sleep(1)

# def get_order(order_ref):
#     act_api_token = ShopSetting.objects.get(id=1)
#     if act_api_token.pf_api_token_time < int(str(time.time())[:10]) or act_api_token.pf_test_mode != setting.get('Other').get('TestModus'):
#         url = 'https://api.prepaidforge.com/v1/1.0/signInWithApi'
#         body = {
#             "email": 'admin@digicod.eu',
#             "password": 'jEz3xfidZi3SccC'
#         }
#         headers = {'Content-Type': 'application/json'}
#         resp = requests.post(url, json=body, headers=headers).json()
#         act_api_token.pf_api_token_time = int(str(resp['tokenValidUntil'])[:10])
#         act_api_token.pf_api_token = resp['apiToken']
#         act_api_token.pf_test_mode = setting.get('Other').get('TestModus')
#         act_api_token.save()
#         act_api_token = ShopSetting.objects.get(id=1)

#     url = f'https://api.prepaidforge.com/v1/1.0/getResponseOfSingleApiCodeRequest'
#     headers = {'Content-Type': 'application/json',
#                'X-PrepaidForge-Api-Token': act_api_token.pf_api_token}
#     body = {"customOrderReference":order_ref}

#     return requests.post(url, data=json.dumps(body), headers=headers)


# # print(get_order("864308-8CJ3YE").text)