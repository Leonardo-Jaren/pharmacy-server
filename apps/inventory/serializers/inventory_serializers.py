from rest_framework import serializers
from apps.inventory.models import Batch, StockMovement


class BatchSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = Batch
        fields = ['id', 'branch', 'branch_name', 'product', 'product_name', 'code',
                  'manufacture_date', 'expiration_date', 'stock_quantity', 'sale_price',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StockMovementSerializer(serializers.ModelSerializer):
    batch_code = serializers.CharField(source='batch.code', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = ['id', 'batch', 'batch_code', 'movement_type', 'quantity', 'reason',
                  'quantity_before', 'quantity_after', 'created_at']
        read_only_fields = ['id', 'created_at', 'quantity_before', 'quantity_after']


class StockAdjustSerializer(serializers.Serializer):
    """Serializer para ajustar stock"""
    quantity = serializers.IntegerField()
    movement_type = serializers.CharField(max_length=50)
    reason = serializers.CharField(max_length=200, required=False, allow_blank=True)
