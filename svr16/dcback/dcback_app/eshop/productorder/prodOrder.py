from eshop.models import PaymentCallback, Jsonfile, Wallet
from eshop_api.utils import wallet_transaction
from eshop.PrepaidForge.Order import pf_product_order
from eshop.order_email_send import orderemail
from eshop.kinguin.order import kinguin_product_order



class ProdOrder:

    def __init__(self, order):
        
        self.order = order

    def do_prod_order(self):
        if self.order.cart.wallet_payment > 0:
                # wallet = Wallet.objects.filter(owner=order.customer).first()
            wallet_transaction(self.order.customer, 'debit', -self.order.cart.wallet_payment,
                                f'Payment for order #{self.order.id}')
        
        pf_roducts = self.order.cart.products.filter(product__brand__wsaler='Prepaidforge')
        kinguin_products = self.order.cart.products.filter(product__brand__wsaler='Kinguin')
        list_res = []
        if pf_roducts:
                pfres = pf_product_order(self.order, pf_roducts)
                list_res.append(pfres)
        if kinguin_products:
                kinres = kinguin_product_order(self.order, kinguin_products)
                list_res.append(kinres)
        for r in list_res:
            if r == 'ok':
                final_res = 'ok'
            else:
                final_res = 'error'
                break
        if final_res == 'ok':
            self.order.status = 'completed'
            self.order.save()
        orderemail(self.order.id)
        self.order.save()
        self.order.cart.save()
        return True
