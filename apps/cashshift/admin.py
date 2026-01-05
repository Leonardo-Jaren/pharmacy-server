from django.contrib import admin
from apps.cashshift.models import CashShift, CashOperation


@admin.register(CashShift)
class CashShiftAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'branch', 'is_closed', 'initial_amount', 'final_amount', 'opened_at')
    list_filter = ('branch', 'is_closed')


@admin.register(CashOperation)
class CashOperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'cash_shift', 'operation_type', 'amount', 'created_at')
    list_filter = ('operation_type',)
