from apps.users.repositories.user_repository import UserRepository
from django.db import transaction


class UserService:
    """Servicio con lógica de negocio para usuarios"""
    
    def __init__(self):
        self.repository = UserRepository()
    
    def get_all_users(self):
        return self.repository.get_all()
    
    def get_user_by_id(self, user_id: int):
        return self.repository.get_by_id(user_id)
    
    def get_user_by_email(self, email: str):
        return self.repository.get_by_email(email)
    
    @transaction.atomic
    def create_user(self, data: dict):
        """Crea un nuevo usuario"""
        password = data.pop('password', None)
        user = self.repository.create(**data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update_user(self, user_id: int, data: dict):
        """Actualiza un usuario existente"""
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        password = data.pop('password', None)
        user = self.repository.update(user, **data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def delete_user(self, user_id: int):
        """Elimina un usuario"""
        user = self.repository.get_by_id(user_id)
        if not user:
            return False
        return self.repository.delete(user)
    
    def search_users(self, query: str):
        """Busca usuarios por nombre"""
        return self.repository.search_by_name(query)
