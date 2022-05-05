from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from core.models import Account
from core.serializers import AccountSerializer, TransactionSerializer
from core.services import get_account_balances_between_period, get_account_extract_between_period
from datetime import datetime


class AccountView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionView(generics.CreateAPIView):
    serializer_class = TransactionSerializer


class ExtractView(generics.ListAPIView):
    serializer_class = TransactionSerializer

    def list(self, request, *args, **kwargs):
        self._validate_query_params()
        query_params = self._get_query_params()

        return Response({
            'transactions': self._get_transactions(query_params),
            'balances': self._get_balances(query_params)
        })

    def _validate_query_params(self):
        required_params = ['account_number', 'start_date', 'end_date']
        validation_errors = {}

        for param in required_params:
            if param not in self.request.query_params:
                validation_errors[param] = f'The param {param} is required'

        if validation_errors:
            raise ValidationError(
                validation_errors, code=status.HTTP_400_BAD_REQUEST)

    def _get_query_params(self):
        query_params = self.request.query_params
        account_number = query_params['account_number']
        operation = query_params['operation']

        def string_to_date(str):
            return datetime.strptime(str, '%Y-%m-%d')

        start_date = string_to_date(query_params['start_date']).replace(
            hour=0, minute=0, second=0)

        end_date = string_to_date(query_params['end_date']).replace(
            hour=23, minute=59, second=59)

        return {
            'account_number': account_number,
            'start_date': start_date,
            'end_date': end_date,
            'operation': operation
        }

    def _get_transactions(self, query_params):
        queryset = get_account_extract_between_period(
            query_params['account_number'],
            query_params['start_date'],
            query_params['end_date'],
            query_params['operation']
        )
        serializer = self.get_serializer(queryset, many=True)
        return serializer.data

    def _get_balances(self, query_params):
        return get_account_balances_between_period(
            query_params['account_number'],
            query_params['start_date'],
            query_params['end_date']
        )
