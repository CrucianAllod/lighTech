from decimal import Decimal

from rest_framework import serializers
from balance.models import Balance


class BalanceTransferSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2, min_value=Decimal('0.01'))
    balance_in = serializers.IntegerField()

    def validate_balance_in(self, value):
        if not Balance.objects.filter(id=value).exists():
            raise serializers.ValidationError("Баланс получателя не найден")
        return value