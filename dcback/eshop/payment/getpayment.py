from eshop.payment.neosurf.neosurf_pay import Neosurf

def getPayment(request, order):
   id = order.uuid
   amount = order.total.get('b')
   currency = order.currency.get('code')
   if order.basket.payment_method.name == 'Neosurf':
      ns = Neosurf()
      resp = ns.neosurf_pay_send(
         orderqs=order, 
         id=id, 
         amount=amount, 
         currency=currency.lower(),
         test='no',
         urlOk="https://front.digicod.eu/checkout?c=ok&oid=" + str(id),
         urlKo="https://front.digicod.eu/rest/cancel/" + str(id),
         urlPending="https://front.digicod.eu/checkout?c=sendorder",
         urlCallback="https://front.digicod.eu/rest/callbck/" + str(id),
         )
      return resp