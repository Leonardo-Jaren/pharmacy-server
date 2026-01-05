from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from apps.users.services.user_service import UserService
from apps.users.serializers.user_serializers import (
    UserSerializer, 
    UserCreateSerializer,
    UserUpdateSerializer
)


class UserViewSet(ViewSet):
    """ViewSet para usuarios usando el servicio"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = UserService()
    
    def list(self, request):
        """Listar todos los usuarios"""
        users = self.service.get_all_users()
        serializer = UserSerializer(users, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def retrieve(self, request, pk=None):
        """Obtener un usuario por ID"""
        user = self.service.get_user_by_id(pk)
        if not user:
            return Response({
                'success': False,
                'message': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    def create(self, request):
        """Crear un nuevo usuario"""
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = self.service.create_user(serializer.validated_data)
        output = UserSerializer(user)
        return Response({
            'success': True,
            'message': 'Usuario creado exitosamente',
            'data': output.data
        }, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        """Actualizar un usuario"""
        serializer = UserUpdateSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = self.service.update_user(pk, serializer.validated_data)
        if not user:
            return Response({
                'success': False,
                'message': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        output = UserSerializer(user)
        return Response({
            'success': True,
            'message': 'Usuario actualizado',
            'data': output.data
        })
    
    def destroy(self, request, pk=None):
        """Eliminar un usuario"""
        deleted = self.service.delete_user(pk)
        if not deleted:
            return Response({
                'success': False,
                'message': 'Usuario no encontrado'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'success': True,
            'message': 'Usuario eliminado'
        })
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Buscar usuarios por nombre"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({
                'success': False,
                'message': 'Parámetro "q" requerido'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        users = self.service.search_users(query)
        serializer = UserSerializer(users, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
