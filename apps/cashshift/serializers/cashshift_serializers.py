from rest_framework import serializers
from apps.cashshift.models import CashShift, CashOperation


class CashOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashOperation
        fields = ['id', 'cash_shift', 'operation_type', 'amount', 'description', 
                  'receipt_image', 'created_at']
        read_only_fields = ['id', 'created_at']


class CashShiftSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = CashShift
        fields = ['id', 'user', 'user_name', 'branch', 'branch_name', 'opened_at', 
                  'closed_at', 'total_sales_cash', 'initial_amount', 'final_amount', 
                  'is_closed', 'created_at']
        read_only_fields = ['id', 'opened_at', 'closed_at', 'total_sales_cash', 'is_closed', 'created_at']


class CloseShiftSerializer(serializers.Serializer):
    """Serializer para cerrar turno"""
    final_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
