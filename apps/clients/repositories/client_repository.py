from .base_repository import BaseRepository
from apps.clients.models import Client
from django.db.models import Q


class ClientRepository(BaseRepository):
    """Repositorio para Client"""
    
    def __init__(self):
        super().__init__(Client)
    
    def get_by_organization(self, organization_id: int):
        return self.model_class.objects.filter(organization_id=organization_id)
    
    def get_by_branch(self, branch_id: int):
        return self.model_class.objects.filter(branch_id=branch_id)
    
    def get_by_document(self, organization_id: int, document_number: str):
        try:
            return self.model_class.objects.get(organization_id=organization_id, document_number=document_number)
        except self.model_class.DoesNotExist:
            return None
    
    def search(self, organization_id: int, query: str):
        return self.model_class.objects.filter(
            organization_id=organization_id
        ).filter(
            Q(name__icontains=query) | 
            Q(document_number__icontains=query) |
            Q(email__icontains=query)
        )
