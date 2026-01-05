from apps.facture.repositories.facture_repository import ElectronicDocumentRepository


class ElectronicDocumentService:
    """Servicio para ElectronicDocumentType"""
    
    def __init__(self):
        self.repository = ElectronicDocumentRepository()
    
    def get_all(self):
        return self.repository.get_all()
    
    def get_by_id(self, doc_id: int):
        return self.repository.get_by_id(doc_id)
    
    def get_by_sale(self, sale_id: int):
        return self.repository.get_by_sale(sale_id)
    
    def create(self, data: dict):
        return self.repository.create(**data)
    
    def update(self, doc_id: int, data: dict):
        doc = self.repository.get_by_id(doc_id)
        if not doc:
            return None
        return self.repository.update(doc, **data)
