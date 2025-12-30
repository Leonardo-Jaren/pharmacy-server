# ========================================
# MODELOS - Aplicando herencia -- ARCHIVO DE EJEMPLO PARA PODER APLIUCAR A CUALQUIER PROYECTO
# ========================================

# usuarios/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class BaseUser(AbstractUser):
    """Usuario base con campos comunes"""
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = False

class Estudiante(models.Model):
    """Perfil específico para estudiantes"""
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    codigo_estudiante = models.CharField(max_length=20, unique=True)
    carrera = models.CharField(max_length=100)
    semestre = models.IntegerField()
    fecha_ingreso = models.DateField()
    
    class Meta:
        db_table = 'usuarios_estudiantes'

class Docente(models.Model):
    """Perfil específico para docentes"""
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    codigo_docente = models.CharField(max_length=20, unique=True)
    departamento = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    fecha_contrato = models.DateField()
    
    class Meta:
        db_table = 'usuarios_docentes'

class NoDocente(models.Model):
    """Perfil específico para personal no docente"""
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    codigo_empleado = models.CharField(max_length=20, unique=True)
    area = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    fecha_contrato = models.DateField()
    
    class Meta:
        db_table = 'usuarios_no_docentes'

# ========================================
# REPOSITORIOS - Principio S: Una responsabilidad por clase
# ========================================

# usuarios/repositories/base_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from django.db.models import QuerySet
from django.core.paginator import Paginator

class BaseRepository(ABC):
    """Repositorio base con operaciones comunes"""
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def get_all(self) -> QuerySet:
        return self.model_class.objects.all()
    
    def get_by_id(self, id: int) -> Optional[Any]:
        try:
            return self.model_class.objects.get(id=id)
        except self.model_class.DoesNotExist:
            return None
    
    def create(self, **kwargs) -> Any:
        return self.model_class.objects.create(**kwargs)
    
    def update(self, instance: Any, **kwargs) -> Any:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    def delete(self, instance: Any) -> bool:
        instance.delete()
        return True
    
    def paginate(self, queryset: QuerySet, page: int, per_page: int = 10):
        paginator = Paginator(queryset, per_page)
        return paginator.get_page(page)

# usuarios/repositories/user_repository.py
from .base_repository import BaseRepository
from ..models import BaseUser
from django.db.models import Q

class UserRepository(BaseRepository):
    """Repositorio para operaciones básicas de usuarios"""
    
    def __init__(self):
        super().__init__(BaseUser)
    
    def get_by_email(self, email: str) -> Optional[BaseUser]:
        try:
            return self.model_class.objects.get(email=email)
        except self.model_class.DoesNotExist:
            return None
    
    def search_by_name(self, query: str) -> QuerySet:
        return self.model_class.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )
    
    def get_active_users(self) -> QuerySet:
        return self.model_class.objects.filter(is_active=True)

# usuarios/repositories/estudiante_repository.py
from .base_repository import BaseRepository
from ..models import Estudiante

class EstudianteRepository(BaseRepository):
    """Repositorio específico para estudiantes"""
    
    def __init__(self):
        super().__init__(Estudiante)
    
    def get_by_codigo(self, codigo: str) -> Optional[Estudiante]:
        try:
            return self.model_class.objects.select_related('user').get(
                codigo_estudiante=codigo
            )
        except self.model_class.DoesNotExist:
            return None
    
    def get_by_carrera(self, carrera: str) -> QuerySet:
        return self.model_class.objects.select_related('user').filter(
            carrera=carrera
        )
    
    def get_by_semestre(self, semestre: int) -> QuerySet:
        return self.model_class.objects.select_related('user').filter(
            semestre=semestre
        )

# usuarios/repositories/docente_repository.py
from .base_repository import BaseRepository
from ..models import Docente

class DocenteRepository(BaseRepository):
    """Repositorio específico para docentes"""
    
    def __init__(self):
        super().__init__(Docente)
    
    def get_by_codigo(self, codigo: str) -> Optional[Docente]:
        try:
            return self.model_class.objects.select_related('user').get(
                codigo_docente=codigo
            )
        except self.model_class.DoesNotExist:
            return None
    
    def get_by_departamento(self, departamento: str) -> QuerySet:
        return self.model_class.objects.select_related('user').filter(
            departamento=departamento
        )

# ========================================
# SERVICES - Lógica de negocio específica
# ========================================

# usuarios/services/base_service.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseUserService(ABC):
    """Servicio base para operaciones de usuarios"""
    
    def __init__(self, repository):
        self.repository = repository
    
    @abstractmethod
    def create_user_profile(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        pass
    
    @abstractmethod
    def get_user_details(self, user_id: int):
        pass

# usuarios/services/estudiante_service.py
from .base_service import BaseUserService
from ..repositories.user_repository import UserRepository
from ..repositories.estudiante_repository import EstudianteRepository
from ..models import BaseUser, Estudiante
from django.db import transaction

class EstudianteService(BaseUserService):
    """Servicio específico para estudiantes"""
    
    def __init__(self):
        self.user_repository = UserRepository()
        self.estudiante_repository = EstudianteRepository()
    
    @transaction.atomic
    def create_user_profile(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crea un usuario y su perfil de estudiante"""
        # Crear usuario base
        user = self.user_repository.create(**user_data)
        
        # Crear perfil de estudiante
        profile_data['user'] = user
        estudiante = self.estudiante_repository.create(**profile_data)
        
        return {
            'user': user,
            'profile': estudiante
        }
    
    def get_user_details(self, user_id: int):
        """Obtiene detalles completos del estudiante"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        try:
            estudiante = self.estudiante_repository.model_class.objects.get(user=user)
            return {
                'user': user,
                'profile': estudiante,
                'type': 'estudiante'
            }
        except self.estudiante_repository.model_class.DoesNotExist:
            return None
    
    def get_estudiantes_by_carrera(self, carrera: str):
        """Obtiene estudiantes por carrera"""
        return self.estudiante_repository.get_by_carrera(carrera)
    
    def update_semestre(self, estudiante_id: int, nuevo_semestre: int):
        """Actualiza el semestre de un estudiante"""
        estudiante = self.estudiante_repository.get_by_id(estudiante_id)
        if estudiante:
            return self.estudiante_repository.update(
                estudiante, 
                semestre=nuevo_semestre
            )
        return None

# usuarios/services/docente_service.py
from .base_service import BaseUserService
from ..repositories.user_repository import UserRepository
from ..repositories.docente_repository import DocenteRepository
from django.db import transaction

class DocenteService(BaseUserService):
    """Servicio específico para docentes"""
    
    def __init__(self):
        self.user_repository = UserRepository()
        self.docente_repository = DocenteRepository()
    
    @transaction.atomic
    def create_user_profile(self, user_data: Dict[str, Any], profile_data: Dict[str, Any]):
        """Crea un usuario y su perfil de docente"""
        user = self.user_repository.create(**user_data)
        profile_data['user'] = user
        docente = self.docente_repository.create(**profile_data)
        
        return {
            'user': user,
            'profile': docente
        }
    
    def get_user_details(self, user_id: int):
        """Obtiene detalles completos del docente"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        try:
            docente = self.docente_repository.model_class.objects.get(user=user)
            return {
                'user': user,
                'profile': docente,
                'type': 'docente'
            }
        except self.docente_repository.model_class.DoesNotExist:
            return None

# ========================================
# SERIALIZERS - Principio S aplicado
# ========================================

# usuarios/serializers/base_serializers.py
from rest_framework import serializers
from ..models import BaseUser

class BaseUserSerializer(serializers.ModelSerializer):
    """Serializer base para usuarios"""
    
    class Meta:
        model = BaseUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'phone_number', 'address', 'created_at']
        read_only_fields = ['id', 'created_at']

# usuarios/serializers/estudiante_serializers.py
from rest_framework import serializers
from .base_serializers import BaseUserSerializer
from ..models import Estudiante

class EstudianteProfileSerializer(serializers.ModelSerializer):
    """Serializer para perfil de estudiante"""
    
    class Meta:
        model = Estudiante
        fields = ['codigo_estudiante', 'carrera', 'semestre', 'fecha_ingreso']

class EstudianteDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para estudiante"""
    user = BaseUserSerializer(read_only=True)
    
    class Meta:
        model = Estudiante
        fields = ['user', 'codigo_estudiante', 'carrera', 'semestre', 'fecha_ingreso']

class EstudianteCreateSerializer(serializers.Serializer):
    """Serializer para crear estudiante"""
    user_data = BaseUserSerializer()
    profile_data = EstudianteProfileSerializer()
    
    def create(self, validated_data):
        from ..services.estudiante_service import EstudianteService
        service = EstudianteService()
        return service.create_user_profile(
            validated_data['user_data'],
            validated_data['profile_data']
        )

# ========================================
# VIEWS - Principio S: Una responsabilidad específica
# ========================================

# usuarios/views/base_views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

class BaseUserViewSet(ModelViewSet):
    """ViewSet base con operaciones comunes"""
    
    def get_success_response(self, data, message="Success"):
        return Response({
            'success': True,
            'message': message,
            'data': data
        }, status=status.HTTP_200_OK)
    
    def get_error_response(self, message, errors=None):
        response_data = {
            'success': False,
            'message': message
        }
        if errors:
            response_data['errors'] = errors
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

# usuarios/views/estudiante_views.py
from rest_framework.decorators import action
from rest_framework import status
from .base_views import BaseUserViewSet
from ..models import Estudiante
from ..serializers.estudiante_serializers import (
    EstudianteDetailSerializer, 
    EstudianteCreateSerializer
)
from ..services.estudiante_service import EstudianteService

class EstudianteViewSet(BaseUserViewSet):
    """ViewSet específico para estudiantes"""
    queryset = Estudiante.objects.select_related('user').all()
    serializer_class = EstudianteDetailSerializer
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = EstudianteService()
    
    def create(self, request):
        """Crear nuevo estudiante"""
        serializer = EstudianteCreateSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return self.get_success_response(
                EstudianteDetailSerializer(result['profile']).data,
                "Estudiante creado exitosamente"
            )
        return self.get_error_response(
            "Error al crear estudiante", 
            serializer.errors
        )
    
    @action(detail=False, methods=['get'])
    def por_carrera(self, request):
        """Obtener estudiantes por carrera"""
        carrera = request.query_params.get('carrera')
        if not carrera:
            return self.get_error_response("Parámetro 'carrera' requerido")
        
        estudiantes = self.service.get_estudiantes_by_carrera(carrera)
        serializer = self.get_serializer(estudiantes, many=True)
        return self.get_success_response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def actualizar_semestre(self, request, pk=None):
        """Actualizar semestre de estudiante"""
        nuevo_semestre = request.data.get('semestre')
        if not nuevo_semestre:
            return self.get_error_response("Campo 'semestre' requerido")
        
        estudiante = self.service.update_semestre(pk, nuevo_semestre)
        if estudiante:
            serializer = self.get_serializer(estudiante)
            return self.get_success_response(serializer.data)
        
        return self.get_error_response("Estudiante no encontrado")

# usuarios/views/docente_views.py
from .base_views import BaseUserViewSet
from ..models import Docente
from ..serializers.docente_serializers import DocenteDetailSerializer
from ..services.docente_service import DocenteService

class DocenteViewSet(BaseUserViewSet):
    """ViewSet específico para docentes"""
    queryset = Docente.objects.select_related('user').all()
    serializer_class = DocenteDetailSerializer
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = DocenteService()

# ========================================
# URLS - Principio S: Rutas organizadas por responsabilidad
# ========================================

# usuarios/urls/__init__.py
from django.urls import path, include

app_name = 'usuarios'

urlpatterns = [
    path('estudiantes/', include('usuarios.urls.estudiante_urls')),
    path('docentes/', include('usuarios.urls.docente_urls')),
    path('no-docentes/', include('usuarios.urls.no_docente_urls')),
]

# usuarios/urls/estudiante_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.estudiante_views import EstudianteViewSet

router = DefaultRouter()
router.register(r'', EstudianteViewSet, basename='estudiante')

urlpatterns = [
    path('', include(router.urls)),
]

# usuarios/urls/docente_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.docente_views import DocenteViewSet

router = DefaultRouter()
router.register(r'', DocenteViewSet, basename='docente')

urlpatterns = [
    path('', include(router.urls)),
]

# ========================================
# CONFIGURACIÓN PRINCIPAL
# ========================================

# proyecto/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/usuarios/', include('usuarios.urls')),
]

# ========================================
# EJEMPLO DE USO EN SETTINGS.PY
# ========================================

# Agregar en INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'usuarios',  # Tu app de usuarios
]

# Configurar el modelo de usuario personalizado
AUTH_USER_MODEL = 'usuarios.BaseUser'