from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from core.models import Account, Transaction
from core.services import create_account, make_deposit, make_withdraw
from core.exceptions import AccountNotExistsException, InsufficientAccountBalanceException, InvalidTransactionValueException


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    def save(self):
        return create_account(**self.validated_data)


class TransactionSerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(write_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['account', 'created_at']

    def save(self):
        transaction_attributes = {
            'account_number': self.validated_data['account_number'],
            'value': self.validated_data['value'],
            'description': self.validated_data['description'],
        }

        operation_handlers = {
            Transaction.DEBIT: make_withdraw,
            Transaction.CREDIT: make_deposit
        }

        operation = self.validated_data['operation']

        try:
            return operation_handlers[operation](**transaction_attributes)
        except (InvalidTransactionValueException, InsufficientAccountBalanceException) as e:
            raise ValidationError({'value': e.message})
        except AccountNotExistsException as e:
            raise ValidationError({'account_number': e.message})
