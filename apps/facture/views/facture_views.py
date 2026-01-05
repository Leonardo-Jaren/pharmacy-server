from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.facture.services.facture_service import ElectronicDocumentService
from apps.facture.serializers.facture_serializers import ElectronicDocumentSerializer


class ElectronicDocumentViewSet(ViewSet):
    """ViewSet para ElectronicDocumentType"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = ElectronicDocumentService()
    
    def list(self, request):
        sale_id = request.query_params.get('sale')
        if sale_id:
            docs = self.service.get_by_sale(sale_id)
        else:
            docs = self.service.get_all()
        serializer = ElectronicDocumentSerializer(docs, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def retrieve(self, request, pk=None):
        doc = self.service.get_by_id(pk)
        if not doc:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ElectronicDocumentSerializer(doc)
        return Response({'success': True, 'data': serializer.data})
    
    def create(self, request):
        serializer = ElectronicDocumentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        doc = self.service.create(serializer.validated_data)
        return Response({'success': True, 'data': ElectronicDocumentSerializer(doc).data}, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        serializer = ElectronicDocumentSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        doc = self.service.update(pk, serializer.validated_data)
        if not doc:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': ElectronicDocumentSerializer(doc).data})
