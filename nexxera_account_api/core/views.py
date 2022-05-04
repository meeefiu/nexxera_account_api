from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Account
from core.serializers import AccountSerializer


@api_view(['GET'])
def list_accounts(request):
    queryset = Account.objects.all()
    serializer = AccountSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_account(request):
    serializer = AccountSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, 201)
