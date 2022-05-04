from decimal import Decimal
from django.db import models

# Create your models here.


class Account(models.Model):
    holder_name = models.CharField(max_length=100)
    number = models.CharField(max_length=5, unique=True)
    balance = models.DecimalField(default=0, max_digits=5, decimal_places=2)


class Transaction(models.Model):
    DEBIT = 'debit'
    CREDIT = 'credit'
    TRANSACTION_TYPES = [
        (CREDIT, 'crédito'),
        (DEBIT, 'débito')
    ]
    value = models.DecimalField(max_digits=5, decimal_places=2)
    operation = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    description = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    account = models.ForeignKey(Account, on_delete=models.RESTRICT)
