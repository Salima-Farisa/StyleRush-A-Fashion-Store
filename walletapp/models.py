from django.db import models
from django.conf import settings
from decimal import Decimal

# Create your models here.

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="wallet")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def credit(self, amount):
        self.balance += Decimal(amount)
        self.save()

    def debit(self, amount):
        amount = Decimal(amount)
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.user.username} - ₹{self.balance}"
