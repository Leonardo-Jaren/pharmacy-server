from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from apps.users.models import User, Role
from apps.users.services.user_service import UserService
from apps.organization.models import Organization, Branch
from apps.organization.services.organization_service import OrganizationService, BranchService


class UserServiceTest(TestCase):
    """Tests para UserService"""
    
    def setUp(self):
        self.service = UserService()
        self.role = Role.objects.create(name='pharmacist')
    
    def test_create_user(self):
        """Prueba crear un usuario"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'role': self.role,
        }
        user = self.service.create_user(data)
        
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_get_user_by_id(self):
        """Prueba obtener usuario por ID"""
        user = User.objects.create_user(username='findme', email='find@test.com', password='test')
        found = self.service.get_user_by_id(user.id)
        
        self.assertIsNotNone(found)
        self.assertEqual(found.username, 'findme')
    
    def test_get_user_not_found(self):
        """Prueba usuario no encontrado"""
        found = self.service.get_user_by_id(99999)
        self.assertIsNone(found)


class OrganizationServiceTest(TestCase):
    """Tests para OrganizationService"""
    
    def setUp(self):
        self.service = OrganizationService()
        self.branch_service = BranchService()
    
    def test_create_organization(self):
        """Prueba crear organización"""
        data = {
            'name': 'Farmacia Test',
            'tax_id': '12345678901'
        }
        org = self.service.create(data)
        
        self.assertIsNotNone(org.id)
        self.assertEqual(org.name, 'Farmacia Test')
    
    def test_create_branch(self):
        """Prueba crear sucursal"""
        org = Organization.objects.create(name='Org Test', tax_id='11111111111')
        data = {
            'organization': org,
            'name': 'Sucursal Central',
            'is_main': True
        }
        branch = self.branch_service.create(data)
        
        self.assertIsNotNone(branch.id)
        self.assertEqual(branch.name, 'Sucursal Central')
        self.assertTrue(branch.is_main)


class UserAPITest(APITestCase):
    """Tests para la API de usuarios"""
    
    def setUp(self):
        self.role = Role.objects.create(name='admin')
        self.user = User.objects.create_user(
            username='apiuser',
            email='api@test.com',
            password='testpass',
            role=self.role
        )
    
    def test_list_users(self):
        """Prueba listar usuarios"""
        response = self.client.get('/api/v1/users/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertGreater(len(response.data['data']), 0)
    
    def test_get_user_detail(self):
        """Prueba obtener detalle de usuario"""
        response = self.client.get(f'/api/v1/users/{self.user.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['data']['username'], 'apiuser')
    
    def test_create_user(self):
        """Prueba crear usuario via API"""
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'newpass123',
            'role': self.role.id
        }
        response = self.client.post('/api/v1/users/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
    
    def test_user_not_found(self):
        """Prueba usuario no encontrado"""
        response = self.client.get('/api/v1/users/99999/')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrganizationAPITest(APITestCase):
    """Tests para la API de organización"""
    
    def test_create_organization(self):
        """Prueba crear organización via API"""
        data = {
            'name': 'Nueva Farmacia',
            'tax_id': '20123456789'
        }
        response = self.client.post('/api/v1/organization/organizations/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
    
    def test_list_organizations(self):
        """Prueba listar organizaciones"""
        Organization.objects.create(name='Farmacia 1', tax_id='11111111111')
        Organization.objects.create(name='Farmacia 2', tax_id='22222222222')
        
        response = self.client.get('/api/v1/organization/organizations/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)
