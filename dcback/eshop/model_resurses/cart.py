from eshop.models import *



class CartModel:
    qs = Cart.objects.all()

    def __init__(self, request) -> None:
        pass

    def update(self):
        qs = self.qs