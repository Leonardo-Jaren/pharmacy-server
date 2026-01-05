from .base_repository import BaseRepository
from apps.inventory.models import Batch, StockMovement
from django.utils import timezone


class BatchRepository(BaseRepository):
    """Repositorio para Batch"""
    
    def __init__(self):
        super().__init__(Batch)
    
    def get_by_branch(self, branch_id: int):
        return self.model_class.objects.filter(branch_id=branch_id)
    
    def get_by_product(self, product_id: int):
        return self.model_class.objects.filter(product_id=product_id)
    
    def get_by_branch_and_product(self, branch_id: int, product_id: int):
        return self.model_class.objects.filter(branch_id=branch_id, product_id=product_id)
    
    def get_expiring_soon(self, branch_id: int, days: int = 30):
        """Obtiene lotes próximos a vencer"""
        future_date = timezone.now().date() + timezone.timedelta(days=days)
        return self.model_class.objects.filter(
            branch_id=branch_id,
            expiration_date__lte=future_date,
            stock_quantity__gt=0
        )
    
    def get_with_stock(self, branch_id: int):
        """Obtiene lotes con stock disponible"""
        return self.model_class.objects.filter(branch_id=branch_id, stock_quantity__gt=0)


class StockMovementRepository(BaseRepository):
    """Repositorio para StockMovement"""
    
    def __init__(self):
        super().__init__(StockMovement)
    
    def get_by_batch(self, batch_id: int):
        return self.model_class.objects.filter(batch_id=batch_id).order_by('-created_at')
