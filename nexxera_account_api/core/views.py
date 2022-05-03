from rest_framework import viewsets, mixins
from core.models import Account
from core.serializers import AccountSerializer


class CreateAndListModelViewSet(viewsets.GenericViewSet,
                                mixins.CreateModelMixin,
                                mixins.ListModelMixin):
    pass


class AccountView(CreateAndListModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
