from apps.cashshift.repositories.cashshift_repository import CashShiftRepository, CashOperationRepository
from django.db import transaction
from django.utils import timezone


class CashShiftService:
    """Servicio para CashShift"""
    
    def __init__(self):
        self.repository = CashShiftRepository()
        self.operation_repository = CashOperationRepository()
    
    def get_all(self):
        return self.repository.get_all()
    
    def get_by_id(self, shift_id: int):
        return self.repository.get_by_id(shift_id)
    
    def get_by_branch(self, branch_id: int):
        return self.repository.get_by_branch(branch_id)
    
    def get_open_shift(self, branch_id: int, user_id: int):
        return self.repository.get_open_shift(branch_id, user_id)
    
    @transaction.atomic
    def open_shift(self, data: dict):
        """Abre un nuevo turno de caja"""
        # Verificar si ya tiene turno abierto
        existing = self.repository.get_open_shift(data['branch'].id, data['user'].id)
        if existing:
            raise ValueError("Ya tienes un turno abierto")
        return self.repository.create(**data)
    
    @transaction.atomic
    def close_shift(self, shift_id: int, final_amount: float):
        """Cierra un turno de caja"""
        shift = self.repository.get_by_id(shift_id)
        if not shift:
            return None
        if shift.is_closed:
            raise ValueError("El turno ya está cerrado")
        
        shift.is_closed = True
        shift.closed_at = timezone.now()
        shift.final_amount = final_amount
        shift.save()
        return shift
    
    def add_sales_amount(self, shift_id: int, amount: float):
        """Suma monto de venta al turno"""
        shift = self.repository.get_by_id(shift_id)
        if not shift or shift.is_closed:
            return None
        shift.total_sales_cash += amount
        shift.save()
        return shift


class CashOperationService:
    """Servicio para CashOperation"""
    
    def __init__(self):
        self.repository = CashOperationRepository()
    
    def get_by_shift(self, cash_shift_id: int):
        return self.repository.get_by_shift(cash_shift_id)
    
    def create(self, data: dict):
        return self.repository.create(**data)
