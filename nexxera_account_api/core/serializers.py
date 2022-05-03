from rest_framework import serializers
from core.models import Account
from core.services import create_account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['holder_name', 'number']

    def create(self, validated_data):
        return create_account(**validated_data)
