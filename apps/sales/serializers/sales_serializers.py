from rest_framework import serializers
from apps.sales.models import Sale, SaleDetail, SalePayment


class SalePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalePayment
        fields = ['id', 'sale', 'payment_method', 'amount', 'created_at']
        read_only_fields = ['id', 'created_at']


class SaleDetailSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    batch_code = serializers.CharField(source='batch.code', read_only=True)
    
    class Meta:
        model = SaleDetail
        fields = ['id', 'sale', 'batch', 'batch_code', 'product', 'product_name',
                  'quantity', 'unit_price', 'subtotal', 'igv_type', 'created_at']
        read_only_fields = ['id', 'created_at']


class SaleSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.name', read_only=True)
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    details = SaleDetailSerializer(many=True, read_only=True)
    payments = SalePaymentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Sale
        fields = ['id', 'branch', 'branch_name', 'cash_shift', 'user', 'user_name',
                  'client', 'client_name', 'total_amount', 'tax_amount', 'discount_amount',
                  'status', 'invoice_number', 'document_type', 'details', 'payments',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SaleCreateSerializer(serializers.Serializer):
    """Serializer para crear venta completa"""
    branch = serializers.IntegerField()
    cash_shift = serializers.IntegerField()
    user = serializers.IntegerField(required=False)
    client = serializers.IntegerField(required=False)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = serializers.CharField(max_length=50)
    invoice_number = serializers.CharField(max_length=100)
    document_type = serializers.CharField(max_length=50)
    
    details = serializers.ListField(child=serializers.DictField())
    payments = serializers.ListField(child=serializers.DictField())
