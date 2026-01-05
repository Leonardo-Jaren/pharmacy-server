from rest_framework import serializers
from apps.organization.models import Organization, Branch, CompanyCredentials, InvoiceSeries


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'tax_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class BranchSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    
    class Meta:
        model = Branch
        fields = ['id', 'organization', 'organization_name', 'name', 'address', 
                  'phone', 'email', 'is_main', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CompanyCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyCredentials
        fields = ['id', 'organization', 'sol_user', 'sol_password', 'sol_token',
                  'certh_path', 'certh_password', 'is_production', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'sol_password': {'write_only': True},
            'certh_password': {'write_only': True},
        }


class InvoiceSeriesSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)
    
    class Meta:
        model = InvoiceSeries
        fields = ['id', 'branch', 'branch_name', 'series', 'current_number', 'created_at']
        read_only_fields = ['id', 'created_at', 'current_number']
