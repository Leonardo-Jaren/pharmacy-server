from django.contrib import admin
from apps.facture.models import ElectronicDocumentType


@admin.register(ElectronicDocumentType)
class ElectronicDocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sale', 'series', 'correlative', 'sunat_status', 'created_at')
    list_filter = ('name', 'sunat_status')
    search_fields = ('series',)
