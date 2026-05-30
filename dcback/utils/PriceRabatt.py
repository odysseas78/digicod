import os, sys, django
sys.path.insert(0, '/home/dcback')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
django.setup()
from eshop.models import PriceRabatt, Wallet, Order, CartProduct
from eshop_api.utils import wallet_transaction
from decimal import Decimal
from loguru import logger

logger.add("logs/PriceRabat.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "PriceRabat")
PriceRabat = logger.bind(name="PriceRabat")
# ordr = Order.objects.filter(customer__user__username='coxah').first()

class RabattCeck:
    from eshop.models import PriceRabatt, Product, Brand, Order, Basket
    def __init__(self, data):
        if type(data) == Order:
            self.cart = data.cart
            self.order = data
        elif type(data) == CartProduct:
            self.cart_product = data
        else:
            self.cart = data
            self.order = None
        self.paymethods = ['Neosurf', 'Flexepin']            

    def cp_check(self):
        products = []
        summ = 0
        res = PriceRabatt.objects.filter(customer=self.cart_product.cart.owner, brand=self.cart_product.product.brand).first()

        if self.cart_product.cart.payment_method.name not in self.paymethods:
            if res:
                rabatt = round(self.cart_product.product.pf_price * (res.brandrabatt / 100) * self.cart_product.qty, 2)
                products.append({'brand_id':self.cart_product.product.brand.id, 'brand_title':self.cart_product.product.brand.title, 'product_id':self.cart_product.product.id, 'product_title':self.cart_product.product.title, 'rabatt':rabatt})
                summ+=rabatt
            else:
                rabatt = round(self.cart_product.product.pf_price * (Decimal(1) / 100) * self.cart_product.qty, 2)
                products.append({'brand_id':self.cart_product.product.brand.id, 'brand_title':self.cart_product.product.brand.title, 'product_id':self.cart_product.product.id, 'product_title':self.cart_product.product.title, 'rabatt':rabatt})
                summ+=rabatt

        return summ
    
    def check(self):
        products = []
        summ = 0
        for proditem in self.cart.products.all():
            product = proditem
            res = PriceRabatt.objects.filter(customer=self.cart.owner, brand=product.brand).first()

            if self.cart.payment_method.name not in self.paymethods:
                try:
                    if res:
                        rabatt = round(product.pf_price * (res.brandrabatt / 100) * self.cart.basket_products.get(str(product.id)).get('qty'), 2)
                        products.append({'brand_id':product.brand.id, 'brand_title':product.brand.title, 'product_id':product.id, 'product_title':product.title, 'rabatt':rabatt})
                        summ+=rabatt
                    else:
                        PriceRabat.info(self.cart)
                        PriceRabat.info(self.cart.basket_products)
                        rabatt = round(product.pf_price * (Decimal(1) / 100) * self.cart.basket_products.get(str(product.id)).get('qty'), 2)
                        products.append({'brand_id':product.brand.id, 'brand_title':product.brand.title, 'product_id':product.id, 'product_title':product.title, 'rabatt':rabatt})
                        summ+=rabatt
                except Exception as d:
                    PriceRabat.info(d)

        return {'products':products, 'summ':summ}

    def walletcredit(self):
        if not self.order:
            return 'No Orderdata'
        summ = self.check().get('summ')
        if summ > 0:
            descript = f'+++ #{self.order.id} | Thank you!'
            wallet = Wallet.objects.filter(description=descript).first()
            if wallet:
                return 'duble transaction'
            tr = wallet_transaction(self.order.customer, 'credit', summ,
                                    descript)
            if tr:
                return 'ok'
            else:
                return 'not credited'
        else:
            return 0
# rch = RabattCeck(ordr)
# print(rch.check())
# print(order.cart.products.all()[0].product.title)