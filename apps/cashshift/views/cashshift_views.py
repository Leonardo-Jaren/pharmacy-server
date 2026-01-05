from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from apps.cashshift.services.cashshift_service import CashShiftService, CashOperationService
from apps.cashshift.serializers.cashshift_serializers import (
    CashShiftSerializer, 
    CashOperationSerializer,
    CloseShiftSerializer
)


class CashShiftViewSet(ViewSet):
    """ViewSet para CashShift"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = CashShiftService()
    
    def list(self, request):
        branch_id = request.query_params.get('branch')
        if branch_id:
            shifts = self.service.get_by_branch(branch_id)
        else:
            shifts = self.service.get_all()
        serializer = CashShiftSerializer(shifts, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def retrieve(self, request, pk=None):
        shift = self.service.get_by_id(pk)
        if not shift:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CashShiftSerializer(shift)
        return Response({'success': True, 'data': serializer.data})
    
    def create(self, request):
        """Abre un nuevo turno"""
        serializer = CashShiftSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            shift = self.service.open_shift(serializer.validated_data)
            return Response({'success': True, 'data': CashShiftSerializer(shift).data}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        """Cierra un turno"""
        serializer = CloseShiftSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            shift = self.service.close_shift(pk, serializer.validated_data['final_amount'])
            if not shift:
                return Response({'success': False, 'message': 'Turno no encontrado'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'success': True, 'data': CashShiftSerializer(shift).data})
        except ValueError as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Obtiene el turno abierto actual"""
        branch_id = request.query_params.get('branch')
        user_id = request.query_params.get('user')
        if not branch_id or not user_id:
            return Response({'success': False, 'message': 'Parámetros branch y user requeridos'}, status=status.HTTP_400_BAD_REQUEST)
        shift = self.service.get_open_shift(branch_id, user_id)
        if not shift:
            return Response({'success': False, 'message': 'No hay turno abierto'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': CashShiftSerializer(shift).data})


class CashOperationViewSet(ViewSet):
    """ViewSet para CashOperation"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = CashOperationService()
    
    def list(self, request):
        shift_id = request.query_params.get('cash_shift')
        if not shift_id:
            return Response({'success': False, 'message': 'Parámetro cash_shift requerido'}, status=status.HTTP_400_BAD_REQUEST)
        operations = self.service.get_by_shift(shift_id)
        serializer = CashOperationSerializer(operations, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def create(self, request):
        serializer = CashOperationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        operation = self.service.create(serializer.validated_data)
        return Response({'success': True, 'data': CashOperationSerializer(operation).data}, status=status.HTTP_201_CREATED)
