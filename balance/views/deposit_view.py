from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from balance.serializers.change_serializer import BalanceChangeSerializer
from balance.services import BalanceService


class BalanceDepositAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BalanceChangeSerializer

    @extend_schema(
        summary="Пополнение баланса",
        request=BalanceChangeSerializer,
        tags=['Balance']
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        balance = request.user.balance

        new_balance = BalanceService.create_deposit(balance, amount)

        return Response({
            'new_balance_amount': new_balance.amount,
        }, status=status.HTTP_200_OK)