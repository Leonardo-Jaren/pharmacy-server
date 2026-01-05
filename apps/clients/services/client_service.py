from apps.clients.repositories.client_repository import ClientRepository


class ClientService:
    """Servicio para Client"""
    
    def __init__(self):
        self.repository = ClientRepository()
    
    def get_all(self):
        return self.repository.get_all()
    
    def get_by_id(self, client_id: int):
        return self.repository.get_by_id(client_id)
    
    def get_by_organization(self, organization_id: int):
        return self.repository.get_by_organization(organization_id)
    
    def get_by_document(self, organization_id: int, document_number: str):
        return self.repository.get_by_document(organization_id, document_number)
    
    def search(self, organization_id: int, query: str):
        return self.repository.search(organization_id, query)
    
    def create(self, data: dict):
        return self.repository.create(**data)
    
    def update(self, client_id: int, data: dict):
        client = self.repository.get_by_id(client_id)
        if not client:
            return None
        return self.repository.update(client, **data)
    
    def delete(self, client_id: int):
        client = self.repository.get_by_id(client_id)
        if not client:
            return False
        return self.repository.delete(client)
