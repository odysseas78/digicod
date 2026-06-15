class Wallet:
    def __init__(self, user_id):
        self.user_id = user_id
        self.balance = 0.0

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Einzahlungsbetrag muss positiv sein.")
        self.balance += amount
        # Hier könnte eine Logfunktion oder eine Datenbankaktualisierung hinzugefügt werden

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Abhebungsbetrag muss positiv sein.")
        if amount > self.balance:
            raise ValueError("Unzureichendes Guthaben.")
        self.balance -= amount
        # Hier könnte eine Logfunktion oder eine Datenbankaktualisierung hinzugefügt werden

    def get_balance(self):
        return self.balance

    def refund(self, amount):
        if amount <= 0:
            raise ValueError("Rückerstattungsbetrag muss positiv sein.")
        self.balance += amount
        # Hier könnte eine Logfunktion oder eine Datenbankaktualisierung hinzugefügt werden


# Beispielverwendung
# wallet = Wallet(user_id=1234)
# wallet.deposit(100.0)
# wallet.withdraw(50.0)
# print(wallet.get_balance())  # sollte 50.0 ausgeben
# wallet.refund(25.0)
# print(wallet.get_balance())  # sollte 75.0 ausgeben

####################################

from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Einzahlungsbetrag muss positiv sein.")
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Abhebungsbetrag muss positiv sein.")
        if amount > self.balance:
            raise ValueError("Unzureichendes Guthaben.")
        self.balance -= amount
        self.save()

    def refund(self, amount):
        if amount <= 0:
            raise ValueError("Rückerstattungsbetrag muss positiv sein.")
        self.balance += amount
        self.save()

# Stellen Sie sicher, dass Sie beim Erstellen eines neuen Benutzers auch ein Wallet für ihn erstellen. 
# Das kann zum Beispiel in einem Signal gemacht werden:
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_wallet(sender, instance, **kwargs):
    instance.wallet.save()

########################################

from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def deposit(self, amount, purpose, transaction_id):
        if self.check_duplicate_transaction(transaction_id):
            raise ValueError("Doppelte Transaktion erkannt.")
        if amount <= 0:
            raise ValueError("Einzahlungsbetrag muss positiv sein.")
        self.balance += amount
        self.save()
        Transaction.objects.create(wallet=self, amount=amount, purpose=purpose, transaction_id=transaction_id)

    def withdraw(self, amount, purpose, transaction_id):
        if self.check_duplicate_transaction(transaction_id):
            raise ValueError("Doppelte Transaktion erkannt.")
        if amount <= 0:
            raise ValueError("Abhebungsbetrag muss positiv sein.")
        if amount > self.balance:
            raise ValueError("Unzureichendes Guthaben.")
        self.balance -= amount
        self.save()
        Transaction.objects.create(wallet=self, amount=-amount, purpose=purpose, transaction_id=transaction_id)

    def refund(self, amount, purpose, transaction_id):
        if self.check_duplicate_transaction(transaction_id):
            raise ValueError("Doppelte Transaktion erkannt.")
        if amount <= 0:
            raise ValueError("Rückerstattungsbetrag muss positiv sein.")
        self.balance += amount
        self.save()
        Transaction.objects.create(wallet=self, amount=amount, purpose=purpose, transaction_id=transaction_id)

    def check_duplicate_transaction(self, transaction_id):
        return Transaction.objects.filter(transaction_id=transaction_id).exists()


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=255, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

# Die vorherigen Signale zur Erstellung des Wallets für einen neuen Benutzer bleiben unverändert.
############################

from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def deposit(self, amount, purpose, transaction_id):
        if self.check_duplicate_transaction(transaction_id):
            raise ValueError("Doppelte Transaktion erkannt.")
        if amount <= 0:
            raise ValueError("Einzahlungsbetrag muss positiv sein.")
        self.balance += amount
        self.save()
        Transaction.objects.create(wallet=self, amount=amount, purpose=purpose, transaction_id=transaction_id)

    def withdraw(self, amount, purpose, transaction_id):
        if self.check_duplicate_transaction(transaction_id):
            raise ValueError("Doppelte Transaktion erkannt.")
        if amount <= 0:
            raise ValueError("Abhebungsbetrag muss positiv sein.")
        if amount > self.balance:
            raise ValueError("Unzureichendes Guthaben.")
        self.balance -= amount
        self.save()
        Transaction.objects.create(wallet=self, amount=-amount, purpose=purpose, transaction_id=transaction_id)

    def refund(self, amount, purpose, transaction_id):
        if self.check_duplicate_transaction(transaction_id):
            raise ValueError("Doppelte Transaktion erkannt.")
        if amount <= 0:
            raise ValueError("Rückerstattungsbetrag muss positiv sein.")
        self.balance += amount
        self.save()
        Transaction.objects.create(wallet=self, amount=amount, purpose=purpose, transaction_id=transaction_id)

    def check_duplicate_transaction(self, transaction_id):
        return Transaction.objects.filter(transaction_id=transaction_id).exists()


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=255, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

# Die vorherigen Signale zur Erstellung des Wallets für einen neuen Benutzer bleiben unverändert.
###########################################

from decimal import Decimal

def migrate_wallet_data():
    # Iteriere über alle Wallet-Einträge im alten Modell
    for old_wallet in OldWalletModel.objects.all():
        
        # Erstelle einen neuen Wallet-Eintrag
        new_wallet, created = Wallet.objects.get_or_create(user=old_wallet.owner.user)
        if created:
            new_wallet.balance = old_wallet.balance
            new_wallet.save()
        
        # Erstelle einen neuen Transaktionseintrag
        Transaction.objects.create(
            wallet=new_wallet,
            amount=old_wallet.amount,
            purpose=old_wallet.typ,
            transaction_id=old_wallet.reference,
        )

# Nachdem die Migration abgeschlossen ist, können Sie das alte Wallet-Modell entfernen.
##########################
locked_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
##############################
def lock_amount(self, amount):
    if amount > self.balance:
        raise ValueError("Betrag zu groß zum Sperren.")
    self.balance -= amount
    self.locked_balance += amount
    self.save()

def unlock_amount(self, amount):
    if amount > self.locked_balance:
        raise ValueError("Betrag zu groß zum Freigeben.")
    self.balance += amount
    self.locked_balance -= amount
    self.save()
###################################
class WalletSegment(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='segments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    description = models.CharField(max_length=255)
    allowed_products = models.ManyToManyField(Product, blank=True) # Falls Sie ein Produkt-Modell haben
    special_conditions = models.JSONField(null=True, blank=True)   # JSON für spezielle Bedingungen
#################################
def add_to_segment(self, amount, description, allowed_products=None, special_conditions=None):
    if amount > self.balance:
        raise ValueError("Nicht genug Guthaben zum Segmentieren.")
    segment = WalletSegment(wallet=self, amount=amount, description=description)
    segment.save()
    
    if allowed_products:
        segment.allowed_products.set(allowed_products)
    
    if special_conditions:
        segment.special_conditions = special_conditions
        segment.save()
    
    self.balance -= amount
    self.save()
#####################################
CONVERSION_RATE = 100  # Zum Beispiel 1 Währungseinheit = 100 Punkte
############################
@property
def points(self):
    return self.balance * CONVERSION_RATE

@points.setter
def points(self, value):
    self.balance = value / CONVERSION_RATE
###################
def add_points(self, points):
    self.balance += points / CONVERSION_RATE
    self.save()

def subtract_points(self, points):
    if self.points < points:
        raise ValueError("Nicht genug Punkte.")
    self.balance -= points / CONVERSION_RATE
    self.save()
