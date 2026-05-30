from eshop.models import *
from apps.accounts.models import *
from eshop.Utilss.PriceRabatt import RabattCeck
from rest_framework import serializers
import decimal
from django.db.models import Q, Avg, Count, Min, Sum, F
from lib.PersistentDictObj import PersistentDictObj
from api.utils.mutations import get_or_create_basket
try:
    from http.cookies import SimpleCookie
except ImportError:
    from Cookie import SimpleCookie # type: ignore
from eshop.Utilss.priceConverter import GlobalDecimalSerializer

def logfn1(name,path='logs/'):
    logger.add(f"{path}/{name}.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == name)
    return logger.bind(name=name)


def getCookies(request):
    cookies = SimpleCookie(request.headers.get('set-cookie'))
    polz = request.COOKIES.get('_polz') if request.COOKIES.get('_polz') else cookies.get('_polz').value if cookies.get('_polz') else None
    ccc = request.COOKIES.get('_ccc') if request.COOKIES.get('_ccc') else cookies.get('_ccc').value if cookies.get('_ccc') else None
    return {'polz':polz, 'ccc':ccc}


class SZ:
   
    def __init__(self):
        self.dbjsonfile = Jsonfile.objects.filter(name='Shopsettings').first()
        self.Shopsettings = PersistentDictObj(dbjsonfile=self.dbjsonfile, dbjsonfileonly=True)
        # self.request = request
        self.cat = self.CategoryS()
        self.cls = """"""

    def getTofx(currency):
        if currency.type == 'crypto':
            if currency.shortname == 'USDT':
                tofix = 2
            else:
                tofix = 8
        else:
            tofix = 2
        return tofix
    
    class CurrencyS(serializers.ModelSerializer):

        class Meta:
            model = Currency
            # fields = '__all__'
            exclude = ['orig_price', 'fee_rate','histori']
    
    class CategoryS(serializers.ModelSerializer):
        
        class Meta:
            model = Category
            fields = '__all__'

    class BrandS(serializers.ModelSerializer):
        
        regions = serializers.SerializerMethodField()
        in_stock = serializers.SerializerMethodField()
        
        class Meta:
            model = Brand
            # read_only = True
            fields = ['id','title','slug','category','image','image2','regions', 'active', 'in_stock']
        
        def get_regions(self, obj):
            regs = set()
            for product in obj.products.filter(active=True, qty__gt=0):
                regs.add(product.region)
            return list(regs)

        def get_in_stock(self, obj):
            resp = False if SZ().Shopsettings.Other.all_no_stock else obj.in_stock
            # resp = obj.in_stock
            return resp
 
        def to_representation(self, instance):
            self.fields['category'] = SZ.CategoryS(many=True)
            return super(SZ.BrandS, self).to_representation(instance)
              
    class ProductS(GlobalDecimalSerializer):
        # price = serializers.SerializerMethodField()
        qty = serializers.SerializerMethodField()
        in_stock = serializers.SerializerMethodField()
        dcoinprice = serializers.SerializerMethodField()
        # brand = SZ().BrandS(read_only=True)

        class Meta:
            model = Product
            fields = [
                'id', 'brand', 'value', 'qty', 'title',
                'price', 'image', 'in_stock','dcoinprice',
                'slug', 'region', 'currency', 'description'
            ]

        def get_qty(self, obj):
            return 0 if SZ().Shopsettings.Other.all_no_stock else obj.qty

        def get_in_stock(self, obj):
            return False if SZ().Shopsettings.Other.all_no_stock else obj.in_stock

        # def get_price(self, obj):
        #     request = self.context.get('request')
        #     basket_id = request.COOKIES.get('_ccc')
        #     fingPrint = request.COOKIES.get('_polz')

        #     if request.user.is_authenticated:
        #         if basket_id and basket_id.isnumeric():
        #             bqs = request.user.customer.basket.filter(in_order=False, id=basket_id).first()
        #         else:
        #             bqs = request.user.customer.basket.filter(in_order=False, fingprint=fingPrint).first()
        #     else:
        #         if basket_id and basket_id.isnumeric():
        #             bqs = SZ.BasketS.Meta.model.objects.filter(in_order=False, id=basket_id).first()
        #         else:
        #             bqs = SZ.BasketS.Meta.model.objects.filter(in_order=False, fingprint=fingPrint).first()

        #     cur = bqs.currency if bqs else SZ.CurrencyS.Meta.model.objects.filter(shortname="EUR").first()
        #     return str(round(obj.price * cur.price, SZ.getTofx(cur)))

        def get_dcoinprice(self, obj):
            dbjsonfile = Jsonfile.objects.filter(name='Shopsettings').first()
            dcoinPrice = dbjsonfile.json.get('Prices').get('dcoinPrice')
            cashbackRate = dbjsonfile.json.get('Prices').get('cashbackRate')
            return str(round(obj.price * decimal.Decimal(cashbackRate) * dcoinPrice, 0))
        
        def to_representation(self, instance):
            self.fields['brand'] = SZ.BrandS()
            # return super(SZ.ProductS, self).to_representation(instance)
            return super().to_representation(instance)
    
    class PayoptionsS(serializers.ModelSerializer):

        class Meta:
            model = Payoptions
            # fields = ('ct_product', 'cart', 'order', 'order_id', 'code', 'serial')
            fields = '__all__'
    
    class PaymentS(serializers.ModelSerializer):

        class Meta:
            model = Payment
            fields = '__all__'

        def to_representation(self, instance):
            self.fields['currencies'] = SZ.CurrencyS(many=True)
            self.fields['payoptions'] = SZ.PayoptionsS(many=True)
            return super(SZ.PaymentS, self).to_representation(instance)
    
    class CartS(serializers.ModelSerializer):

        limit = serializers.SerializerMethodField()
        # rabatt = serializers.SerializerMethodField()
        final_price = serializers.SerializerMethodField()
        order_final_price = serializers.SerializerMethodField()
        process_fee = serializers.SerializerMethodField()

        def get_limit(self, obj):
            res = False
            if obj.final_price > 500:
                res = True
            return res
        
        # def get_rabatt(self, obj):
        #     rch = RabattCeck(obj)
        #     return rch.check().get('summ')
        
        def get_final_price(self, obj):
            # obj.final_price * obj.currency.price
            return str(round(obj.final_price * obj.currency.price, SZ.getTofx(obj.currency)))
        
        def get_order_final_price(self, obj):
            # obj.order_final_price * obj.currency.price
            return str(round(obj.order_final_price * obj.currency.price, SZ.getTofx(obj.currency)))
        
        def get_process_fee(self, obj):
            obj.process_fee * obj.currency.price
            return str(round(obj.process_fee * obj.currency.price, SZ.getTofx(obj.currency)))

        class Meta:
            model = Cart
            fields = '__all__'
            
        def to_representation(self, instance):
            self.fields['payment_method'] = SZ.PaymentS()
            self.fields['currency'] = SZ.CurrencyS()
            self.fields['products'] = SZ.CartProductS(many=True)
            
            return super(SZ.CartS, self).to_representation(instance)
        
    class BasketS(GlobalDecimalSerializer):
        
        limit = serializers.SerializerMethodField()
        # rabatt = serializers.SerializerMethodField()
        # total_price = serializers.SerializerMethodField()
        # final_price = serializers.SerializerMethodField()
        # process_fee = serializers.SerializerMethodField()
        basket_products = serializers.SerializerMethodField()

        def get_limit(self, obj):
            llqs = Limit.objects.filter(category='basket')
            def fn1(lqs):
                lnew = lqs.filter(name='new').first().cart
                lglobal = lqs.filter(name='global').first().cart
                isuser = self.context.get('request').user
                if isuser.is_authenticated:
                    luser = lqs.filter(customer__user__username=isuser.username).first()
                    if luser:
                        return luser.cart
                    elif isuser.customer.status == 'new':
                        return lnew
                    else:
                        return lglobal
                else:
                    return lnew
            return str(round(fn1(llqs) * obj.currency.price, SZ.getTofx(obj.currency)))
        
        # def get_rabatt(self, obj):
        #     rch = RabattCeck(obj)
        #     return rch.check().get('summ')
        
        # def get_total_price(self, obj):
        #     # obj.final_price * obj.currency.price
        #     return str(round(obj.total_price * obj.currency.price, SZ.getTofx(obj.currency)))
        
        # def get_final_price(self, obj):
        #     # obj.order_final_price * obj.currency.price
        #     return str(round(obj.final_price * obj.currency.price, SZ.getTofx(obj.currency)))
        
        # def get_process_fee(self, obj):
        #     # obj.process_fee * obj.currency.price
        #     return str(round(obj.process_fee * obj.currency.price, SZ.getTofx(obj.currency)))
        
        def get_basket_products(self, obj):
            if SZ().Shopsettings.Other.all_no_stock:
                obj.basket_products = {}
                obj.products.clear()
                obj.save()
            else:
                for k in obj.basket_products.keys():
                    obj.basket_products[k]['price']=round(obj.basket_products[k]['price'] * float(obj.currency.price), SZ.getTofx(obj.currency))
                    obj.basket_products[k]['total']=round(obj.basket_products[k]['total'] * float(obj.currency.price), SZ.getTofx(obj.currency))
            return obj.basket_products

        class Meta:
            model = Basket
            # fields = '__all__'
            exclude = ['created_at','updated_at','fingprint','in_order', 'addinfo']
            
        def to_representation(self, instance):
            self.fields['payment_method'] = SZ.PaymentS()
            self.fields['currency'] = SZ.CurrencyS()
            self.fields['products'] = SZ.ProductS(many=True)
            
            return super(SZ.BasketS, self).to_representation(instance)
            
    class CartProductS(serializers.ModelSerializer):

        # rabatt = serializers.SerializerMethodField()
        final_price = serializers.SerializerMethodField()
        order_price = serializers.SerializerMethodField()

        # def get_rabatt(self, obj):
        #     rch = RabattCeck(obj)
        #     return rch.cp_check()
        
        def get_final_price(self, obj):
            return str(round(obj.final_price * obj.cart.currency.price, SZ.getTofx(obj.cart.currency)))
        
        def get_order_price(self, obj):
            return str(round(obj.order_price * obj.cart.currency.price, SZ.getTofx(obj.cart.currency)))

        class Meta:
            model = CartProduct
            fields = '__all__'
            
        def to_representation(self, instance):
            self.fields['product'] = SZ.ProductS()
            self.fields['currency'] = SZ.CurrencyS()
            self.fields['product_codes'] = SZ.ProductCodeS(many=True)
            return super(SZ.CartProductS, self).to_representation(instance)
    
    class ProductCodeS(serializers.ModelSerializer):

        class Meta:
            model = ProductCode
            fields = '__all__'

    class VerificationS(serializers.ModelSerializer):

        class Meta:
            model = Verification
            fields = '__all__'
            # fields = ['id', 'product', 'qty', 'final_price']
        
    class UserS(serializers.ModelSerializer):

        class Meta:
            model = User
            # fields = '__all__'
            fields = ['id','email','last_name','first_name']

    class CustomerS(serializers.ModelSerializer):
        
        ip_country = serializers.SerializerMethodField()
        
        class Meta:
            model = Customer
            # fields = '__all__'
            fields = ['city','country_code','date_of_birth','phone','postal_code','street','status','ip_country']
        
        def get_ip_country(self, obj):
            if self.context.get('request').user.is_authenticated:
                qs = LoginStatistic.objects.filter(username=self.context.get('request').user.username).last()
                return qs.country_code
            else:
                return None
            # return str(round(obj.final_price * obj.cart.currency.price, SZ.getTofx(obj.cart.currency)))
            
        def to_representation(self, instance):
            self.fields['user'] = SZ.UserS()
            return super(SZ.CustomerS, self).to_representation(instance)
                
    class OrderS(serializers.ModelSerializer):
        cods = serializers.SerializerMethodField()
        class Meta:
            model = Order
            # fields = '__all__'
            fields = [
            'id',
            'pay_currency',
            'pay_amount',
            'status',
            'created_at',
            'cart',
            'cods'
        ]
        def to_representation(self, instance):
            self.fields['cart'] = SZ.CartS()
            self.fields['pay_currency'] = SZ.CurrencyS()
            return super(SZ.OrderS, self).to_representation(instance)
        
        def get_cods(self, obj):
            qs = ProductCode.objects.filter(order=obj, created_at__gte='2023-05-01')
            if qs:
                for i in qs:
                    if len(i.code) > 3 and not i.code.startswith('Sorry,'):
                        return 1
                return 0
            else:
                return 0

    class OrdersS(serializers.ModelSerializer):
        cods = serializers.SerializerMethodField()
        class Meta:
            model = Orders
            # fields = '__all__'
            fields = [
            'id',
            'uuid',
            'currency',
            'total',
            'status',
            'created_at',
            'basket',
            'cods',
            'responsedata'
        ]
        def to_representation(self, instance):
            self.fields['basket'] = SZ.BasketS()
            self.fields['currency'] = SZ.CurrencyS()
            return super(SZ.OrdersS, self).to_representation(instance)
        
        def get_cods(self, obj):
            qs = ProductCodes.objects.filter(order=obj, created_at__gte='2023-05-01')
            if qs:
                for i in qs:
                    if len(i.code) > 3 and not i.code.startswith('Sorry,'):
                        return 1
                return 0
            else:
                return 0

    class CoinWalletDepositS(serializers.ModelSerializer):
        class Meta:
            model = CoinWalletDeposit
            # fields = '__all__'
            fields = [
            'id',
            'uuid',
            'currency',
            'total',
            'status',
            'created_at',
            'coinwallet',
            'responsedata'
        ]
        def to_representation(self, instance):
            self.fields['coinwallet'] = SZ.CoinWalletS()
            self.fields['currency'] = SZ.CurrencyS()
            return super(SZ.CoinWalletDepositS, self).to_representation(instance)
            
    class WalletOrderS(serializers.ModelSerializer):
      
        class Meta:
            model = WalletOrder
            # fields = '__all__'
            fields = [
            'id',
            'price',
            'fee',
            'total_price',
            'currency',
            'payment_method',
            'status',
            'created_at'
        ]
        def to_representation(self, instance):
            self.fields['payment_method'] = SZ.PaymentS()
            self.fields['currency'] = SZ.CurrencyS()
            return super(SZ.WalletOrderS, self).to_representation(instance)
        
    class WalletS(serializers.ModelSerializer):
        
        class Meta:
            model = Wallet
            # fields = '__all__'
            fields = [
            'id',
            'amount',
            'typ',
            'description',
            'balance',
            'created_at'
        ]
            
    class CoinWalletS(GlobalDecimalSerializer):
        # balance = serializers.SerializerMethodField()
        dcbalance = serializers.SerializerMethodField()
        class Meta:
            model = CoinWallet
            # fields = '__all__'
            fields = [
            'id',
            'user',
            'balance',
            'dcbalance',
            'locked_balance'
        ]
            
        # def get_balance(self, obj):
        #     if self.context.get('request').user.is_authenticated:
        #         fprint = getCookies(self.context.get('request')).get('polz')
        #         basketid = getCookies(self.context.get('request')).get('ccc')
        #         print(f'fprint: {fprint}  |  basketid: {basketid}')
                
        #         c = self.context.get('request').user.customer.basket.filter(in_order=False).filter(
        #             Q(fingprint=getCookies(self.context.get('request')).get('polz')) | Q(id=getCookies(self.context.get('request')).get('ccc'))
        #             ).first()
        #         if not c:
        #             bqs = SZ.BasketS.Meta.model.objects.all()
        #             get_basket = get_or_create_basket(self.context.get('request'), bqs)
        #             print(f'get_basket: {get_basket}')
        #             c = get_basket
        #         print(f'C: {c}')
        #         cur = c.currency
        #     return str(round(obj.balance * cur.price, SZ.getTofx(cur)))
        
        def get_dcbalance(self, obj):
            dbjsonfile = Jsonfile.objects.filter(name='Shopsettings').first()
            dcoinPrice = dbjsonfile.json.get('Prices').get('dcoinPrice')
            return str(round(obj.balance * decimal.Decimal(dcoinPrice)))
            
    class CoinWalletTransactionS(GlobalDecimalSerializer):
        # amount = serializers.SerializerMethodField()
        dcamount = serializers.SerializerMethodField()
        class Meta:
            model = CoinWalletTransaction
            # fields = '__all__'
            fields = [
            'id',
            'wallet',
            'amount',
            'purpose',
            'description',
            'transaction_id',
            'dcamount',
            'created_at'
        ]
            
        # def get_amount(self, obj):
        #     if self.context.get('request').user.is_authenticated:
        #         c = self.context.get('request').user.customer.basket.filter(in_order=False).filter(
        #             Q(fingprint=getCookies(self.context.get('request')).get('polz')) | Q(id=getCookies(self.context.get('request')).get('ccc'))
        #             ).first()
        #         if c:
        #             cur = c.currency
                
        #     return str(round(obj.amount * cur.price, SZ.getTofx(cur)))
        
        def get_dcamount(self, obj):
            dbjsonfile = Jsonfile.objects.filter(name='Shopsettings').first()
            dcoinPrice = dbjsonfile.json.get('Prices').get('dcoinPrice')
            return str(round(obj.amount * dcoinPrice))
                    
        def to_representation(self, instance):
            self.fields['wallet'] = SZ.CoinWalletS()
            return super(SZ.CoinWalletTransactionS, self).to_representation(instance)


    class CoinWalletSegmentS(serializers.ModelSerializer):
            amount = serializers.SerializerMethodField()
            dcamount = serializers.SerializerMethodField()
            class Meta:
                model = CoinWalletSegment
                fields = '__all__'
            
            def get_dcamount(self, obj):
                dbjsonfile = Jsonfile.objects.filter(name='Shopsettings').first()
                dcoinPrice = dbjsonfile.json.get('Prices').get('dcoinPrice')
                return str(round(obj.amount * dcoinPrice))
                        
            def to_representation(self, instance):
                self.fields['wallet'] = SZ.CoinWalletS()
                return super(SZ.TransactionS, self).to_representation(instance)