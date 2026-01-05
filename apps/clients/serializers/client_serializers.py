from rest_framework import serializers
from apps.clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'organization', 'branch', 'name', 'email', 'phone', 
                  'address', 'document_type', 'document_number', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
