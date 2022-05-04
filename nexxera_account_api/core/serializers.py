from rest_framework import serializers
from core.models import Account, Transaction
from core.services import create_account, make_deposit, make_withdraw


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
        if self.validated_data['operation'] == Transaction.DEBIT:
            return make_withdraw(**transaction_attributes)
        if self.validated_data['operation'] == Transaction.CREDIT:
            return make_deposit(**transaction_attributes)
