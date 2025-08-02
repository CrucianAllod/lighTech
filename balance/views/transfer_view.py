from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from balance.models import Balance
from balance.serializers.transfer_serializer import BalanceTransferSerializer
from balance.services import BalanceService


class BalanceTransferAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = BalanceTransferSerializer

    @extend_schema(
        summary="Перевод с баланса",
        request=BalanceTransferSerializer,
        tags=['Balance']
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        balance_in_id = serializer.validated_data['balance_in']

        balance_out = request.user.balance
        balance_in = Balance.objects.get(id=balance_in_id)

        try:
            new_balance_out = BalanceService.create_transfer(balance_out, balance_in, amount)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'new_balance_amount': new_balance_out.amount,
        }, status=status.HTTP_200_OK)