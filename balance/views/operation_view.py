from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from balance.models import BalanceOperation
from balance.serializers.operation_serializer import BalanceOperationSerializer

@extend_schema_view(
    get=extend_schema(
        tags=['Balance'],
        summary='Список операций с балансом пользователя',
    )
)
class OperationListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BalanceOperationSerializer

    def get_queryset(self):
        return BalanceOperation.objects.filter(balance=self.request.user.balance).order_by('-created_at')