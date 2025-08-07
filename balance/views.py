from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from balance.models import BalanceOperation
from balance.serializers.change_serializer import BalanceChangeSerializer
from balance.serializers.operation_serializer import BalanceOperationSerializer
from balance.serializers.transfer_serializer import BalanceTransferSerializer
from balance.services import BalanceService


class BalanceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,]

    @extend_schema(
        summary="Пополнение баланса",
        request=BalanceChangeSerializer,
        tags=['Balance']
    )
    @action(detail=False, methods=['post'], url_path='deposit')
    def deposit(self, request):
        serializer = BalanceChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']
        new_balance = BalanceService.deposit(request.user, amount)
        return Response({'new_balance_amount': new_balance.amount}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Снятие с баланса",
        request=BalanceChangeSerializer,
        tags=['Balance']
    )
    @action(detail=False, methods=['post'], url_path='withdraw')
    def withdraw(self, request):
        serializer = BalanceChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']
        try:
            new_balance = BalanceService.withdraw(request.user, amount)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'new_balance_amount': new_balance.amount}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Перевод с баланса",
        request=BalanceTransferSerializer,
        tags=['Balance']
    )
    @action(detail=False, methods=['post'], url_path='transfer')
    def transfer(self, request):
        serializer = BalanceTransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['amount']
        balance_in_id = serializer.validated_data['balance_in']
        try:
            new_balance = BalanceService.transfer(request.user, balance_in_id, amount)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'new_balance_amount': new_balance.amount}, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Список операций с балансом пользователя',
        responses=BalanceOperation,
        tags=['Balance']
    )
    @action(detail=False, methods=['get'], url_path='operations')
    def operations(self, request):
        cache_key = f'balance_operations_user_{request.user.id}'
        cached_data = cache.get(cache_key)

        if cached_data is None:
            operations = BalanceOperation.objects.filter(balance=request.user.balance).order_by('-created_at')
            serializer = BalanceOperationSerializer(operations, many=True)
            data = serializer.data
            cache.set(cache_key, data, timeout=60)
        else:
            data = cached_data

        return Response(data)