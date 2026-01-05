from django.contrib import admin
from apps.inventory.models import Batch, StockMovement


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'product', 'branch', 'stock_quantity', 'expiration_date')
    list_filter = ('branch', 'product')
    search_fields = ('code',)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('id', 'batch', 'movement_type', 'quantity', 'quantity_before', 'quantity_after', 'created_at')
    list_filter = ('movement_type',)
