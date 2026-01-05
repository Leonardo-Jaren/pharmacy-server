from django.contrib import admin
from apps.sales.models import Sale, SaleDetail, SalePayment


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice_number', 'branch', 'client', 'total_amount', 'status', 'created_at')
    list_filter = ('branch', 'status', 'document_type')
    search_fields = ('invoice_number',)


@admin.register(SaleDetail)
class SaleDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale', 'product', 'quantity', 'unit_price', 'subtotal')
    list_filter = ('sale',)


@admin.register(SalePayment)
class SalePaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'sale', 'payment_method', 'amount', 'created_at')
    list_filter = ('payment_method',)
