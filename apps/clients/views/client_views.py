from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from apps.clients.services.client_service import ClientService
from apps.clients.serializers.client_serializers import ClientSerializer


class ClientViewSet(ViewSet):
    """ViewSet para Client"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = ClientService()
    
    def list(self, request):
        org_id = request.query_params.get('organization')
        if org_id:
            clients = self.service.get_by_organization(org_id)
        else:
            clients = self.service.get_all()
        serializer = ClientSerializer(clients, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def retrieve(self, request, pk=None):
        client = self.service.get_by_id(pk)
        if not client:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClientSerializer(client)
        return Response({'success': True, 'data': serializer.data})
    
    def create(self, request):
        serializer = ClientSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        client = self.service.create(serializer.validated_data)
        return Response({'success': True, 'data': ClientSerializer(client).data}, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        serializer = ClientSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        client = self.service.update(pk, serializer.validated_data)
        if not client:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': ClientSerializer(client).data})
    
    def destroy(self, request, pk=None):
        if not self.service.delete(pk):
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'message': 'Eliminado'})
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        org_id = request.query_params.get('organization')
        query = request.query_params.get('q', '')
        if not org_id:
            return Response({'success': False, 'message': 'Parámetro organization requerido'}, status=status.HTTP_400_BAD_REQUEST)
        clients = self.service.search(org_id, query)
        serializer = ClientSerializer(clients, many=True)
        return Response({'success': True, 'data': serializer.data})
