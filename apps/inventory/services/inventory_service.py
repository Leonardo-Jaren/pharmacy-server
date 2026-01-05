from apps.inventory.repositories.inventory_repository import BatchRepository, StockMovementRepository
from django.db import transaction


class BatchService:
    """Servicio para Batch"""
    
    def __init__(self):
        self.repository = BatchRepository()
        self.movement_repository = StockMovementRepository()
    
    def get_all(self):
        return self.repository.get_all()
    
    def get_by_id(self, batch_id: int):
        return self.repository.get_by_id(batch_id)
    
    def get_by_branch(self, branch_id: int):
        return self.repository.get_by_branch(branch_id)
    
    def get_by_product(self, product_id: int):
        return self.repository.get_by_product(product_id)
    
    def get_expiring_soon(self, branch_id: int, days: int = 30):
        return self.repository.get_expiring_soon(branch_id, days)
    
    def get_with_stock(self, branch_id: int):
        return self.repository.get_with_stock(branch_id)
    
    def create(self, data: dict):
        return self.repository.create(**data)
    
    def update(self, batch_id: int, data: dict):
        batch = self.repository.get_by_id(batch_id)
        if not batch:
            return None
        return self.repository.update(batch, **data)
    
    @transaction.atomic
    def adjust_stock(self, batch_id: int, quantity: int, movement_type: str, reason: str = None):
        """Ajusta el stock y crea un movimiento"""
        batch = self.repository.get_by_id(batch_id)
        if not batch:
            return None
        
        quantity_before = batch.stock_quantity
        quantity_after = quantity_before + quantity
        
        if quantity_after < 0:
            raise ValueError("Stock no puede ser negativo")
        
        # Actualizar batch
        batch.stock_quantity = quantity_after
        batch.save()
        
        # Crear movimiento
        self.movement_repository.create(
            batch=batch,
            movement_type=movement_type,
            quantity=quantity,
            reason=reason,
            quantity_before=quantity_before,
            quantity_after=quantity_after
        )
        
        return batch


class StockMovementService:
    """Servicio para StockMovement"""
    
    def __init__(self):
        self.repository = StockMovementRepository()
    
    def get_by_batch(self, batch_id: int):
        return self.repository.get_by_batch(batch_id)
