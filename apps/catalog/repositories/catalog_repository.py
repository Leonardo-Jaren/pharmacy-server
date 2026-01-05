from .base_repository import BaseRepository
from apps.catalog.models import Product, Category
from django.db.models import Q


class ProductRepository(BaseRepository):
    """Repositorio para Product"""
    
    def __init__(self):
        super().__init__(Product)
    
    def get_by_organization(self, organization_id: int):
        return self.model_class.objects.filter(organization_id=organization_id)
    
    def get_by_category(self, category_id: int):
        return self.model_class.objects.filter(category_id=category_id)
    
    def get_by_barcode(self, organization_id: int, barcode: str):
        try:
            return self.model_class.objects.get(organization_id=organization_id, barcode=barcode)
        except self.model_class.DoesNotExist:
            return None
    
    def search(self, organization_id: int, query: str):
        return self.model_class.objects.filter(
            organization_id=organization_id
        ).filter(
            Q(name__icontains=query) | 
            Q(generic_name__icontains=query) |
            Q(barcode__icontains=query)
        )


class CategoryRepository(BaseRepository):
    """Repositorio para Category"""
    
    def __init__(self):
        super().__init__(Category)
    
    def get_by_organization(self, organization_id: int):
        return self.model_class.objects.filter(organization_id=organization_id)
