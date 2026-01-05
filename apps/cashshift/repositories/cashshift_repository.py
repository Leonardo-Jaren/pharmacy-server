from .base_repository import BaseRepository
from apps.cashshift.models import CashShift, CashOperation


class CashShiftRepository(BaseRepository):
    """Repositorio para CashShift"""
    
    def __init__(self):
        super().__init__(CashShift)
    
    def get_by_branch(self, branch_id: int):
        return self.model_class.objects.filter(branch_id=branch_id).order_by('-opened_at')
    
    def get_by_user(self, user_id: int):
        return self.model_class.objects.filter(user_id=user_id).order_by('-opened_at')
    
    def get_open_shift(self, branch_id: int, user_id: int):
        """Obtiene turno abierto del usuario en la sucursal"""
        try:
            return self.model_class.objects.get(
                branch_id=branch_id, 
                user_id=user_id, 
                is_closed=False
            )
        except self.model_class.DoesNotExist:
            return None
    
    def get_open_shifts_by_branch(self, branch_id: int):
        return self.model_class.objects.filter(branch_id=branch_id, is_closed=False)


class CashOperationRepository(BaseRepository):
    """Repositorio para CashOperation"""
    
    def __init__(self):
        super().__init__(CashOperation)
    
    def get_by_shift(self, cash_shift_id: int):
        return self.model_class.objects.filter(cash_shift_id=cash_shift_id).order_by('-created_at')
