from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from balance.serializers.change_serializer import BalanceChangeSerializer
from balance.services import BalanceService


class BalanceWithdrawAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BalanceChangeSerializer

    @extend_schema(
        summary="Снятие с баланса",
        request=BalanceChangeSerializer,
        tags=['Balance']
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        balance = request.user.balance

        try:
            new_balance = BalanceService.create_withdraw(balance, amount)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'new_balance_amount': new_balance.amount,
        }, status=status.HTTP_200_OK)