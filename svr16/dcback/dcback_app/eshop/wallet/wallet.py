from django.db import models
from django.contrib.auth.models import User
from django.db import transaction
from decimal import Decimal
from eshop.wallet.utils import random_code
from django.db.models import Sum
# Calculate the total price of all books




class CoinWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coinwallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    locked_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    json = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} | [{self.balance} - {round(self.balance * 33)}]  | {self.locked_balance}'


    ##########################################################################################################################################
    @transaction.atomic
    def deposit(self, amount, purpose, description='', segment=None):
        # kjhkjhkjhkj kjh kjh kjhk jhkjhkjhkj hkjh kjhk
        transaction_id=f'D{random_code(16,True,True,True,False)}'
        if self.check_duplicate_transaction(transaction_id):
            raise ValueError("Doppelte Transaktion erkannt.")
        if amount <= 0:
            raise ValueError("Einzahlungsbetrag muss positiv sein.")
        self.balance += Decimal(amount)
        self.save()
        
        if segment:
            segmentobj = self.segmrnt_get_or_create(description=segment.get('description'), amount=Decimal(amount), 
                                       allowed_products=segment.get('allowed_products'), special_conditions=segment.get('special_conditions'))
        else:
            segmentobj = self.segmrnt_get_or_create(description='free', amount=Decimal(amount))
            
        CoinWalletTransaction.objects.create(wallet=self, amount=amount, purpose=purpose, 
                                             description=description, transaction_id=transaction_id, segment=segmentobj)
    ##########################################################################################################################################
        
        
    
    @transaction.atomic
    def withdraw(self, amount, purpose, description='', segment=None,
                 transaction_id=f'W{random_code(16,True,True,True,False)}'):
        if self.check_duplicate_transaction(transaction_id):
            raise ValueError("Doppelte Transaktion erkannt.")
        if amount <= 0:
            raise ValueError("Abhebungsbetrag muss positiv sein.")
        if amount > self.balance:
            raise ValueError("Unzureichendes Guthaben.")
        self.balance -= Decimal(amount)
        self.save()
        if segment:
            segmentobj = self.segmrnt_get_or_create(description=segment.get('description'), amount=-Decimal(amount), 
                                       allowed_products=segment.get('allowed_products'), special_conditions=segment.get('special_conditions'))
        else:
            segmentobj = self.segmrnt_get_or_create(description='free', amount=-Decimal(amount))
        CoinWalletTransaction.objects.create(wallet=self, amount=-amount, purpose=purpose, description=description, 
                                             transaction_id=transaction_id, segment=segmentobj)
        
        

    @transaction.atomic
    def refund(self, amount, purpose, description='', transaction_id=f'R{random_code(16,True,True,True,False)}'):
        if self.check_duplicate_transaction(transaction_id):
            raise ValueError("Doppelte Transaktion erkannt.")
        if amount <= 0:
            raise ValueError("Rückerstattungsbetrag muss positiv sein.")
        self.balance += Decimal(amount)
        self.save()
        CoinWalletTransaction.objects.create(wallet=self, amount=amount, purpose=purpose, description=description, transaction_id=transaction_id)

    def check_duplicate_transaction(self, transaction_id):
        return CoinWalletTransaction.objects.filter(transaction_id=transaction_id).exists()

    @transaction.atomic
    def lock_amount(self, amount):
        if amount > self.balance:
            raise ValueError("Betrag zu groß zum Sperren.")
        if amount <= 0:
            raise ValueError("Betrag muss positiv sein.")
        self.balance -= amount
        self.locked_balance += Decimal(amount)
        self.save()
    
    @transaction.atomic
    def unlock_amount(self, amount):
        if amount > self.locked_balance:
            raise ValueError("Betrag zu groß zum Freigeben.")
        if amount <= 0:
            raise ValueError("Betrag muss positiv sein.")
        self.balance += amount
        self.locked_balance -= Decimal(amount)
        self.save()
        
    @transaction.atomic
    def segmrnt_get_or_create(self, description, amount, allowed_products=None, special_conditions=None):
        amount = Decimal(amount)
        #     raise ValueError("Nicht genug Guthaben zum Segmentieren.")
        segmentobj, created =  CoinWalletSegment.objects.get_or_create(
                wallet=self,
                description=description, 
                defaults={
                    'amount':amount,
                    'special_conditions':special_conditions,
                    })
        if not created:
            segmentobj.description = description
            segmentobj.amount = segmentobj.amount + Decimal(amount)
            segmentobj.special_conditions = special_conditions
            segmentobj.save()
        if allowed_products:
            segmentobj.allowed_products.set(allowed_products)
            segmentobj.save()
        qs = CoinWalletSegment.objects.filter(wallet=self)
        total = qs.aggregate(Sum('amount'))
        print(f'{total} - {round(self.balance,2)}')
        return segmentobj
        

        
    @transaction.atomic
    def create_user_wallet(self, user):
        wallet = CoinWallet.objects.create(user=user, balance=Decimal(0.0))
        wallet.save()
        return wallet
    class Meta:
        app_label = 'eshop'
        
        
class CoinWalletSegment(models.Model):
    wallet = models.ForeignKey(CoinWallet, on_delete=models.CASCADE, related_name='wallet_segment')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    description = models.CharField(max_length=255)
    allowed_products = models.ManyToManyField('Product', blank=True) # Falls Sie ein Produkt-Modell haben
    special_conditions = models.JSONField(null=True, blank=True)   # JSON für spezielle Bedingungen
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'
        
        

class CoinWalletTransaction(models.Model):
    wallet = models.ForeignKey(CoinWallet, on_delete=models.CASCADE, related_name='wallet_transaction')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    transaction_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    segment = models.ForeignKey(CoinWalletSegment, on_delete=models.CASCADE, blank=True, null=True, related_name='segment_transaction')
    json = models.JSONField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        app_label = 'eshop'



from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_coinwallet(sender, instance, created, **kwargs):
    # print(f"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW:  {sender} - {instance} - {created} - {kwargs}")
    if created:
        if not CoinWallet.objects.filter(user=instance).first():
            wallet = CoinWallet().create_user_wallet(user=instance)
            amount = Decimal(round(20/33, 2))
            wallet.deposit(amount,  "Welcome!", '', {'amount':amount, 'description':'cashbach_bonus'})
            wallet.save()
   

@receiver(post_save, sender=User)
def save_user_coinwallet(sender, instance, **kwargs):
    pass
    # print(f"DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD:    {sender} - {instance} - {kwargs}")
    # instance.coinwallet.save()

########################################

