from apps.organization.repositories.organization_repository import (
    OrganizationRepository, 
    BranchRepository,
    CompanyCredentialsRepository,
    InvoiceSeriesRepository
)
from django.db import transaction


class OrganizationService:
    """Servicio para Organization"""
    
    def __init__(self):
        self.repository = OrganizationRepository()
    
    def get_all(self):
        return self.repository.get_all()
    
    def get_by_id(self, org_id: int):
        return self.repository.get_by_id(org_id)
    
    def create(self, data: dict):
        return self.repository.create(**data)
    
    def update(self, org_id: int, data: dict):
        org = self.repository.get_by_id(org_id)
        if not org:
            return None
        return self.repository.update(org, **data)
    
    def delete(self, org_id: int):
        org = self.repository.get_by_id(org_id)
        if not org:
            return False
        return self.repository.delete(org)


class BranchService:
    """Servicio para Branch"""
    
    def __init__(self):
        self.repository = BranchRepository()
    
    def get_all(self):
        return self.repository.get_all()
    
    def get_by_id(self, branch_id: int):
        return self.repository.get_by_id(branch_id)
    
    def get_by_organization(self, organization_id: int):
        return self.repository.get_by_organization(organization_id)
    
    def create(self, data: dict):
        return self.repository.create(**data)
    
    def update(self, branch_id: int, data: dict):
        branch = self.repository.get_by_id(branch_id)
        if not branch:
            return None
        return self.repository.update(branch, **data)
    
    def delete(self, branch_id: int):
        branch = self.repository.get_by_id(branch_id)
        if not branch:
            return False
        return self.repository.delete(branch)


class CompanyCredentialsService:
    """Servicio para CompanyCredentials"""
    
    def __init__(self):
        self.repository = CompanyCredentialsRepository()
    
    def get_by_organization(self, organization_id: int):
        return self.repository.get_by_organization(organization_id)
    
    def create(self, data: dict):
        return self.repository.create(**data)
    
    def update(self, cred_id: int, data: dict):
        cred = self.repository.get_by_id(cred_id)
        if not cred:
            return None
        return self.repository.update(cred, **data)


class InvoiceSeriesService:
    """Servicio para InvoiceSeries"""
    
    def __init__(self):
        self.repository = InvoiceSeriesRepository()
    
    def get_by_branch(self, branch_id: int):
        return self.repository.get_by_branch(branch_id)
    
    def create(self, data: dict):
        return self.repository.create(**data)
    
    @transaction.atomic
    def get_next_number(self, branch_id: int, series: str):
        """Obtiene y actualiza el siguiente número de serie"""
        invoice_series = self.repository.get_by_series(branch_id, series)
        if not invoice_series:
            return None
        invoice_series.current_number += 1
        invoice_series.save()
        return invoice_series.current_number
