from rest_framework import serializers
from core.models import Account
from core.services import create_account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    def save(self):
        return create_account(**self.validated_data)
