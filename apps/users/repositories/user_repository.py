from .base_repository import BaseRepository
from apps.users.models import User
from django.db.models import Q

class UserRepository(BaseRepository):
    """Repositorio para operaciones de usuarios"""
    
    def __init__(self):
        super().__init__(User)
    
    def get_by_email(self, email: str):
        try:
            return self.model_class.objects.get(email=email)
        except self.model_class.DoesNotExist:
            return None
    
    def get_by_username(self, username: str):
        try:
            return self.model_class.objects.get(username=username)
        except self.model_class.DoesNotExist:
            return None
    
    def search_by_name(self, query: str):
        return self.model_class.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )
    
    def get_active_users(self):
        return self.model_class.objects.filter(is_active=True)
