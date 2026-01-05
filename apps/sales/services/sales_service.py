from apps.sales.repositories.sales_repository import SaleRepository, SaleDetailRepository, SalePaymentRepository
from apps.inventory.repositories.inventory_repository import BatchRepository
from apps.cashshift.services.cashshift_service import CashShiftService
from django.db import transaction


class SaleService:
    """Servicio para Sale"""
    
    def __init__(self):
        self.repository = SaleRepository()
        self.detail_repository = SaleDetailRepository()
        self.payment_repository = SalePaymentRepository()
        self.batch_repository = BatchRepository()
        self.cashshift_service = CashShiftService()
    
    def get_all(self):
        return self.repository.get_all()
    
    def get_by_id(self, sale_id: int):
        return self.repository.get_by_id(sale_id)
    
    def get_by_branch(self, branch_id: int):
        return self.repository.get_by_branch(branch_id)
    
    def get_by_client(self, client_id: int):
        return self.repository.get_by_client(client_id)
    
    def get_by_cash_shift(self, cash_shift_id: int):
        return self.repository.get_by_cash_shift(cash_shift_id)
    
    @transaction.atomic
    def create_sale(self, sale_data: dict, details: list, payments: list):
        """Crea una venta completa con detalles y pagos"""
        # Crear venta
        sale = self.repository.create(**sale_data)
        
        # Crear detalles y descontar stock
        for detail in details:
            detail['sale'] = sale
            self.detail_repository.create(**detail)
            
            # Descontar stock del lote
            batch = self.batch_repository.get_by_id(detail['batch'].id)
            if batch:
                batch.stock_quantity -= detail['quantity']
                batch.save()
        
        # Crear pagos
        for payment in payments:
            payment['sale'] = sale
            self.payment_repository.create(**payment)
        
        # Actualizar turno de caja si es efectivo
        cash_amount = sum(p['amount'] for p in payments if p['payment_method'] == 'cash')
        if cash_amount > 0:
            self.cashshift_service.add_sales_amount(sale_data['cash_shift'].id, float(cash_amount))
        
        return sale
    
    def cancel_sale(self, sale_id: int):
        """Cancela una venta"""
        sale = self.repository.get_by_id(sale_id)
        if not sale:
            return None
        sale.status = 'canceled'
        sale.save()
        return sale


class SaleDetailService:
    """Servicio para SaleDetail"""
    
    def __init__(self):
        self.repository = SaleDetailRepository()
    
    def get_by_sale(self, sale_id: int):
        return self.repository.get_by_sale(sale_id)


class SalePaymentService:
    """Servicio para SalePayment"""
    
    def __init__(self):
        self.repository = SalePaymentRepository()
    
    def get_by_sale(self, sale_id: int):
        return self.repository.get_by_sale(sale_id)
