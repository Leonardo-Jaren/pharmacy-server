from rest_framework import serializers
from apps.catalog.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'organization', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'organization', 'category', 'category_name', 'name', 'generic_name',
                  'description', 'barcode', 'presentation', 'base_price', 'stack_quantity',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
