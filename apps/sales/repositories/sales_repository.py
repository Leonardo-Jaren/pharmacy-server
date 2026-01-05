from .base_repository import BaseRepository
from apps.sales.models import Sale, SaleDetail, SalePayment


class SaleRepository(BaseRepository):
    """Repositorio para Sale"""
    
    def __init__(self):
        super().__init__(Sale)
    
    def get_by_branch(self, branch_id: int):
        return self.model_class.objects.filter(branch_id=branch_id).order_by('-created_at')
    
    def get_by_client(self, client_id: int):
        return self.model_class.objects.filter(client_id=client_id).order_by('-created_at')
    
    def get_by_cash_shift(self, cash_shift_id: int):
        return self.model_class.objects.filter(cash_shift_id=cash_shift_id).order_by('-created_at')
    
    def get_by_status(self, branch_id: int, status: str):
        return self.model_class.objects.filter(branch_id=branch_id, status=status)


class SaleDetailRepository(BaseRepository):
    """Repositorio para SaleDetail"""
    
    def __init__(self):
        super().__init__(SaleDetail)
    
    def get_by_sale(self, sale_id: int):
        return self.model_class.objects.filter(sale_id=sale_id)


class SalePaymentRepository(BaseRepository):
    """Repositorio para SalePayment"""
    
    def __init__(self):
        super().__init__(SalePayment)
    
    def get_by_sale(self, sale_id: int):
        return self.model_class.objects.filter(sale_id=sale_id)
