from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from apps.inventory.services.inventory_service import BatchService, StockMovementService
from apps.inventory.serializers.inventory_serializers import (
    BatchSerializer, 
    StockMovementSerializer,
    StockAdjustSerializer
)


class BatchViewSet(ViewSet):
    """ViewSet para Batch"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = BatchService()
    
    def list(self, request):
        branch_id = request.query_params.get('branch')
        product_id = request.query_params.get('product')
        
        if product_id:
            batches = self.service.get_by_product(product_id)
        elif branch_id:
            batches = self.service.get_by_branch(branch_id)
        else:
            batches = self.service.get_all()
        
        serializer = BatchSerializer(batches, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def retrieve(self, request, pk=None):
        batch = self.service.get_by_id(pk)
        if not batch:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BatchSerializer(batch)
        return Response({'success': True, 'data': serializer.data})
    
    def create(self, request):
        serializer = BatchSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        batch = self.service.create(serializer.validated_data)
        return Response({'success': True, 'data': BatchSerializer(batch).data}, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        serializer = BatchSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        batch = self.service.update(pk, serializer.validated_data)
        if not batch:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': BatchSerializer(batch).data})
    
    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        """Ajusta el stock de un lote"""
        serializer = StockAdjustSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            batch = self.service.adjust_stock(
                pk, 
                serializer.validated_data['quantity'],
                serializer.validated_data['movement_type'],
                serializer.validated_data.get('reason')
            )
            if not batch:
                return Response({'success': False, 'message': 'Lote no encontrado'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'success': True, 'data': BatchSerializer(batch).data})
        except ValueError as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def expiring(self, request):
        """Obtiene lotes próximos a vencer"""
        branch_id = request.query_params.get('branch')
        days = int(request.query_params.get('days', 30))
        if not branch_id:
            return Response({'success': False, 'message': 'Parámetro branch requerido'}, status=status.HTTP_400_BAD_REQUEST)
        batches = self.service.get_expiring_soon(branch_id, days)
        serializer = BatchSerializer(batches, many=True)
        return Response({'success': True, 'data': serializer.data})


class StockMovementViewSet(ViewSet):
    """ViewSet para StockMovement"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = StockMovementService()
    
    def list(self, request):
        batch_id = request.query_params.get('batch')
        if not batch_id:
            return Response({'success': False, 'message': 'Parámetro batch requerido'}, status=status.HTTP_400_BAD_REQUEST)
        movements = self.service.get_by_batch(batch_id)
        serializer = StockMovementSerializer(movements, many=True)
        return Response({'success': True, 'data': serializer.data})
