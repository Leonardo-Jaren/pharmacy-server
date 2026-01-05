from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from apps.sales.services.sales_service import SaleService, SaleDetailService, SalePaymentService
from apps.sales.serializers.sales_serializers import (
    SaleSerializer, 
    SaleDetailSerializer, 
    SalePaymentSerializer,
    SaleCreateSerializer
)


class SaleViewSet(ViewSet):
    """ViewSet para Sale"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = SaleService()
    
    def list(self, request):
        branch_id = request.query_params.get('branch')
        client_id = request.query_params.get('client')
        cash_shift_id = request.query_params.get('cash_shift')
        
        if cash_shift_id:
            sales = self.service.get_by_cash_shift(cash_shift_id)
        elif client_id:
            sales = self.service.get_by_client(client_id)
        elif branch_id:
            sales = self.service.get_by_branch(branch_id)
        else:
            sales = self.service.get_all()
        
        serializer = SaleSerializer(sales, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def retrieve(self, request, pk=None):
        sale = self.service.get_by_id(pk)
        if not sale:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = SaleSerializer(sale)
        return Response({'success': True, 'data': serializer.data})
    
    def create(self, request):
        """Crea una venta completa"""
        serializer = SaleCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        details = data.pop('details')
        payments = data.pop('payments')
        
        # Convertir IDs a objetos
        from apps.organization.models import Branch
        from apps.cashshift.models import CashShift
        from apps.users.models import User
        from apps.clients.models import Client
        from apps.inventory.models import Batch
        from apps.catalog.models import Product
        
        data['branch'] = Branch.objects.get(id=data['branch'])
        data['cash_shift'] = CashShift.objects.get(id=data['cash_shift'])
        if 'user' in data:
            data['user'] = User.objects.get(id=data['user'])
        if 'client' in data:
            data['client'] = Client.objects.get(id=data['client'])
        
        # Convertir detalles
        for detail in details:
            detail['batch'] = Batch.objects.get(id=detail['batch'])
            detail['product'] = Product.objects.get(id=detail['product'])
        
        try:
            sale = self.service.create_sale(data, details, payments)
            return Response({'success': True, 'data': SaleSerializer(sale).data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancela una venta"""
        sale = self.service.cancel_sale(pk)
        if not sale:
            return Response({'success': False, 'message': 'Venta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': SaleSerializer(sale).data})


class SaleDetailViewSet(ViewSet):
    """ViewSet para SaleDetail"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = SaleDetailService()
    
    def list(self, request):
        sale_id = request.query_params.get('sale')
        if not sale_id:
            return Response({'success': False, 'message': 'Parámetro sale requerido'}, status=status.HTTP_400_BAD_REQUEST)
        details = self.service.get_by_sale(sale_id)
        serializer = SaleDetailSerializer(details, many=True)
        return Response({'success': True, 'data': serializer.data})
