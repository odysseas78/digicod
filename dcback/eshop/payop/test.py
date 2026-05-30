import os
import tempfile
# import django

# os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
# django.setup()
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# from shop import settings
from loguru import logger
import json
import re
from collections import OrderedDict
from datetime import datetime, timezone, timedelta
import requests
import hashlib
import jsons
import time
from requests.structures import CaseInsensitiveDict
# import mouse
# import socks
# ip='127.0.0.10' # change your proxy's ip
# port = 6000 # change your proxy's port
# socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, port)
# socket.socket = socks.socksocket


# print(mouse.on_click(print('kkkk'), args=()))


from django.core.mail import send_mail

from functions import *



def default_pay_send(id, amount, currency, urlOk, urlKo, email, name, ip):
    items = [{'id':str(id),'name':'Digipoints top-up', 'price': str(amount)}]

    result = create_invoice(paymentMethod='4526', amount=str(amount), currency=currency, items=items, orderid=str(id), 
                            useremail=email, fullname=name, resultUrl=urlOk, failPath=urlKo).json()
    identifier = result.get('data')
    pprint(identifier)
    result = get_invoice(identifier).json()
    pprint(result)
    resp = create_checkout(invid=identifier, customer={'email': email, 'name': name, 'ip':ip}, paymentMethod=None, payCurrency=currency, card=None, orderid=str(id))
    result = resp.json()
    pprint(result)
    result = check_inv_status(identifier).json()
    pprint(result)
    # order = result.get('data').get('form').get('fields')
    # post_data = json.dumps(order, separators=(',', ':'))
    # url = result.get('data').get('form').get('url')
    # resp = requests.post(url, data=post_data, headers={'content-type': 'application/json'})
    # pprint(resp)

# default_pay_send(id='TEST456f7k89', amount=124.86, currency='EUR', 
#                 urlOk='https://digicod.eu' + "/payments/" + 'TEST456f7k89', urlKo='https://digicod.eu'+ f"/cancel/TEST456f7k89", 
#                 email='o.martasidis@yahoo.de', name='Odysseas'+'Martasidis', ip='193.26.158.12')

# print(get_paymethod())
# gg = get_paymethod().get('data')
# for i in gg:
#     print(f"{i.get('title')} - {i.get('type')} - {i.get('logo')}")

    

# from reportlab.pdfgen import canvas
# import urllib.request
# import json
# import io
# from PIL import Image

# data = json.load(open('payopmethods.json'))
# c = canvas.Canvas("pamethods.pdf")
# k = 0

# for item in data.get('data'):
#     # Setzen Sie hier die Schriftart und die Größe
#     c.setFont("Helvetica", 12)
#     # Titel
#     c.drawString(100, 800, f"title: {item.get('title')}")
#     # Währungen
#     currencies_str = ", ".join(item.get('currencies'))
#     c.drawString(100, 780, f"currencies: {currencies_str}")
#     # Länder
#     countries_str = ", ".join(item.get('countries'))
#     c.drawString(100, 760, f"countries: {countries_str}")
    
#     image_url = item.get('logo')
#     req = urllib.request.Request(
#         image_url, 
#         headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
#     )
#     try:
#         image_data = urllib.request.urlopen(req).read()
#         image = Image.open(io.BytesIO(image_data))
#         # Konvertiere PIL Image in ein BytesIO-Objekt
#          # Temporäre Datei für das Bild erstellen
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_image:
#             image.save(tmp_image, format='PNG')
#             tmp_image_path = tmp_image.name
#     except urllib.error.HTTPError as e:
#         print(f"Fehler beim Herunterladen des Bildes: {e}")
#         continue  # Zum nächsten Bild übergehen oder eine alternative Aktion durchführen
#     # Bild in das PDF einfügen
#     c.drawImage(tmp_image_path, 100, 720, width=30, height=30)
#     c.showPage()
#     k+=1
#     if k > 3:
#         break
# c.save()







# html = '''<!DOCTYPE html>
# <html lang="en">
# <head>
#   <meta charset="UTF-8">
#   <meta http-equiv="X-UA-Compatible" content="IE=edge">
#   <meta name="viewport" content="width=device-width, initial-scale=1.0">
#   <title>Invoice</title>

# </head>
# <body style="height: 350mm;width: 210mm;padding: 15px;margin: 0 auto;overflow: hidden;font-family: Arial, Helvetica, sans-serif;">
#     {0}
# </body>
# </html>'''


# finalhtml = ''''''
# with open('payopmethods.json', 'r') as f:
#     jss = json.loads(f.read())
    
# for item in jss.get('data'):
#     finalhtml += f'''<div style="display: flex;" >
#       <img src="{item.get('logo')}" width="60px" height="60px" style="margin: 5px;" />
#       <div style="margin: 5px;" >
#         <div>Title: <b>{item.get('title')}</b></div>
#         <div>Countries: <b>{item.get('countries')}</b></div>
#         <div>Currencies: <b>{item.get('currencies')}</b></div>
#       </div>
#     </div>
#     <hr/>
#     '''

# with open('/home/dcback/eshop/payop/paymethods.html', 'w') as f2:
#     f2.write(html.format(finalhtml))



# print(html.format(finalhtml))