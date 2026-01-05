from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.organization.services.organization_service import (
    OrganizationService,
    BranchService,
    CompanyCredentialsService,
    InvoiceSeriesService
)
from apps.organization.serializers.organization_serializers import (
    OrganizationSerializer,
    BranchSerializer,
    CompanyCredentialsSerializer,
    InvoiceSeriesSerializer
)


class OrganizationViewSet(ViewSet):
    """ViewSet para Organization"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = OrganizationService()
    
    def list(self, request):
        orgs = self.service.get_all()
        serializer = OrganizationSerializer(orgs, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def retrieve(self, request, pk=None):
        org = self.service.get_by_id(pk)
        if not org:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrganizationSerializer(org)
        return Response({'success': True, 'data': serializer.data})
    
    def create(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        org = self.service.create(serializer.validated_data)
        return Response({'success': True, 'data': OrganizationSerializer(org).data}, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        serializer = OrganizationSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        org = self.service.update(pk, serializer.validated_data)
        if not org:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': OrganizationSerializer(org).data})
    
    def destroy(self, request, pk=None):
        if not self.service.delete(pk):
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'message': 'Eliminado'})


class BranchViewSet(ViewSet):
    """ViewSet para Branch"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = BranchService()
    
    def list(self, request):
        org_id = request.query_params.get('organization')
        if org_id:
            branches = self.service.get_by_organization(org_id)
        else:
            branches = self.service.get_all()
        serializer = BranchSerializer(branches, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def retrieve(self, request, pk=None):
        branch = self.service.get_by_id(pk)
        if not branch:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BranchSerializer(branch)
        return Response({'success': True, 'data': serializer.data})
    
    def create(self, request):
        serializer = BranchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        branch = self.service.create(serializer.validated_data)
        return Response({'success': True, 'data': BranchSerializer(branch).data}, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        serializer = BranchSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        branch = self.service.update(pk, serializer.validated_data)
        if not branch:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': BranchSerializer(branch).data})
    
    def destroy(self, request, pk=None):
        if not self.service.delete(pk):
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'message': 'Eliminado'})


class InvoiceSeriesViewSet(ViewSet):
    """ViewSet para InvoiceSeries"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = InvoiceSeriesService()
    
    def list(self, request):
        branch_id = request.query_params.get('branch')
        if branch_id:
            series = self.service.get_by_branch(branch_id)
        else:
            series = []
        serializer = InvoiceSeriesSerializer(series, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def create(self, request):
        serializer = InvoiceSeriesSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        series = self.service.create(serializer.validated_data)
        return Response({'success': True, 'data': InvoiceSeriesSerializer(series).data}, status=status.HTTP_201_CREATED)
