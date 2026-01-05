from .base_repository import BaseRepository
from apps.organization.models import Organization, Branch, CompanyCredentials, InvoiceSeries


class OrganizationRepository(BaseRepository):
    """Repositorio para Organization"""
    
    def __init__(self):
        super().__init__(Organization)
    
    def get_by_tax_id(self, tax_id: str):
        try:
            return self.model_class.objects.get(tax_id=tax_id)
        except self.model_class.DoesNotExist:
            return None
    
    def get_by_name(self, name: str):
        try:
            return self.model_class.objects.get(name=name)
        except self.model_class.DoesNotExist:
            return None


class BranchRepository(BaseRepository):
    """Repositorio para Branch"""
    
    def __init__(self):
        super().__init__(Branch)
    
    def get_by_organization(self, organization_id: int):
        return self.model_class.objects.filter(organization_id=organization_id)
    
    def get_main_branch(self, organization_id: int):
        try:
            return self.model_class.objects.get(organization_id=organization_id, is_main=True)
        except self.model_class.DoesNotExist:
            return None


class CompanyCredentialsRepository(BaseRepository):
    """Repositorio para CompanyCredentials"""
    
    def __init__(self):
        super().__init__(CompanyCredentials)
    
    def get_by_organization(self, organization_id: int):
        return self.model_class.objects.filter(organization_id=organization_id)


class InvoiceSeriesRepository(BaseRepository):
    """Repositorio para InvoiceSeries"""
    
    def __init__(self):
        super().__init__(InvoiceSeries)
    
    def get_by_branch(self, branch_id: int):
        return self.model_class.objects.filter(branch_id=branch_id)
    
    def get_by_series(self, branch_id: int, series: str):
        try:
            return self.model_class.objects.get(branch_id=branch_id, series=series)
        except self.model_class.DoesNotExist:
            return None
