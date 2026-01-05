from rest_framework import serializers
from apps.facture.models import ElectronicDocumentType


class ElectronicDocumentSerializer(serializers.ModelSerializer):
    sale_invoice = serializers.CharField(source='sale.invoice_number', read_only=True)
    
    class Meta:
        model = ElectronicDocumentType
        fields = ['id', 'name', 'sale', 'sale_invoice', 'series', 'correlative',
                  'xml_link', 'cdr_link', 'sunat_status', 'hash_code', 'qr_data',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
