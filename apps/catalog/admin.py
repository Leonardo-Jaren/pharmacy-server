from django.contrib import admin
from apps.catalog.models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization', 'created_at')
    list_filter = ('organization',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'barcode', 'category', 'base_price', 'stack_quantity')
    list_filter = ('organization', 'category')
    search_fields = ('name', 'barcode', 'generic_name')
