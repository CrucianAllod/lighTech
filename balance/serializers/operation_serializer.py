from rest_framework import serializers

from balance.models import BalanceOperation


class BalanceOperationSerializer(serializers.ModelSerializer):
    operation_display = serializers.CharField(source='get_operation_display', read_only=True)

    class Meta:
        model = BalanceOperation
        fields = [
            'id',
            'operation',
            'operation_display',
            'operation_amount',
            'operation_result',
            'related_balance',
            'created_at',
        ]
