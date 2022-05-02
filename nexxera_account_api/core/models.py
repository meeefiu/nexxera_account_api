from django.db import models

# Create your models here.


class Account(models.Model):
    holder_name = models.CharField(max_length=100)
    number = models.CharField(max_length=5, unique=True)
    balance = models.DecimalField(default=0, max_digits=5, decimal_places=2)


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'crédito'),
        ('PAYMENT', 'débito')
    ]
    value = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    operation = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.RESTRICT)
