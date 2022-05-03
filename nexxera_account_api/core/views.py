from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Account
from core import services
from core.serializers import AccountSerializer


@api_view(['GET'])
def list_accounts(request):
    queryset = Account.objects.all()
    serializer = AccountSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_account(request):
    account_attributes = {
        'holder_name': request.data.get('holder_name'),
        'number': request.data.get('number')
    }
    account = services.create_account(**account_attributes)
    serializer = AccountSerializer(account)
    return Response(serializer.data)
