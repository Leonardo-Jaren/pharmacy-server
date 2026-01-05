from .base_repository import BaseRepository
from apps.facture.models import ElectronicDocumentType


class ElectronicDocumentRepository(BaseRepository):
    """Repositorio para ElectronicDocumentType"""
    
    def __init__(self):
        super().__init__(ElectronicDocumentType)
    
    def get_by_sale(self, sale_id: int):
        return self.model_class.objects.filter(sale_id=sale_id)
    
    def get_by_series(self, series: str):
        return self.model_class.objects.filter(series=series).order_by('-correlative')
