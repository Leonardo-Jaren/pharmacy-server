from django.contrib import admin
from apps.clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'document_number', 'email', 'phone', 'organization')
    list_filter = ('organization', 'branch')
    search_fields = ('name', 'document_number', 'email')
