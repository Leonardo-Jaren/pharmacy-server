from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from apps.catalog.services.catalog_service import ProductService, CategoryService
from apps.catalog.serializers.catalog_serializers import ProductSerializer, CategorySerializer


class ProductViewSet(ViewSet):
    """ViewSet para Product"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = ProductService()
    
    def list(self, request):
        org_id = request.query_params.get('organization')
        category_id = request.query_params.get('category')
        
        if category_id:
            products = self.service.get_by_category(category_id)
        elif org_id:
            products = self.service.get_by_organization(org_id)
        else:
            products = self.service.get_all()
        
        serializer = ProductSerializer(products, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def retrieve(self, request, pk=None):
        product = self.service.get_by_id(pk)
        if not product:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response({'success': True, 'data': serializer.data})
    
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        product = self.service.create(serializer.validated_data)
        return Response({'success': True, 'data': ProductSerializer(product).data}, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        serializer = ProductSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        product = self.service.update(pk, serializer.validated_data)
        if not product:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': ProductSerializer(product).data})
    
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
        products = self.service.search(org_id, query)
        serializer = ProductSerializer(products, many=True)
        return Response({'success': True, 'data': serializer.data})


class CategoryViewSet(ViewSet):
    """ViewSet para Category"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = CategoryService()
    
    def list(self, request):
        org_id = request.query_params.get('organization')
        if org_id:
            categories = self.service.get_by_organization(org_id)
        else:
            categories = self.service.get_all()
        serializer = CategorySerializer(categories, many=True)
        return Response({'success': True, 'data': serializer.data})
    
    def retrieve(self, request, pk=None):
        category = self.service.get_by_id(pk)
        if not category:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response({'success': True, 'data': serializer.data})
    
    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        category = self.service.create(serializer.validated_data)
        return Response({'success': True, 'data': CategorySerializer(category).data}, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        serializer = CategorySerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        category = self.service.update(pk, serializer.validated_data)
        if not category:
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'data': CategorySerializer(category).data})
    
    def destroy(self, request, pk=None):
        if not self.service.delete(pk):
            return Response({'success': False, 'message': 'No encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True, 'message': 'Eliminado'})
