from django.contrib import admin
from apps.organization.models import Organization, Branch, CompanyCredentials, InvoiceSeries


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tax_id', 'created_at')
    search_fields = ('name', 'tax_id')


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization', 'is_main', 'created_at')
    list_filter = ('organization', 'is_main')
    search_fields = ('name',)


@admin.register(CompanyCredentials)
class CompanyCredentialsAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'is_production', 'created_at')
    list_filter = ('is_production',)


@admin.register(InvoiceSeries)
class InvoiceSeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'branch', 'series', 'current_number')
    list_filter = ('branch',)
