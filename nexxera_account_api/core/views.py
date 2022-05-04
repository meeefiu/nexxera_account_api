from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.models import Account, Transaction
from core.serializers import AccountSerializer, TransactionSerializer


@api_view(['GET'])
def list_accounts(request):
    queryset = Account.objects.all()
    serializer = AccountSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_account(request):
    perform_create(AccountSerializer, request.data)
    return Response({'message': 'Account created'}, status.HTTP_201_CREATED)


@api_view(['POST'])
def create_transaction(request):
    perform_create(TransactionSerializer, request.data)
    return Response({'message': 'Transaction created'}, status.HTTP_201_CREATED)


def perform_create(serializer_class, data):
    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()


@api_view(['GET'])
def list_extract(request):
    queryset = Transaction.objects.all()
    serializer = TransactionSerializer(queryset, many=True)
    return Response(serializer.data)
