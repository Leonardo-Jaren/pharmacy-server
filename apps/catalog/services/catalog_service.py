from apps.catalog.repositories.catalog_repository import ProductRepository, CategoryRepository


class ProductService:
    """Servicio para Product"""
    
    def __init__(self):
        self.repository = ProductRepository()
    
    def get_all(self):
        return self.repository.get_all()
    
    def get_by_id(self, product_id: int):
        return self.repository.get_by_id(product_id)
    
    def get_by_organization(self, organization_id: int):
        return self.repository.get_by_organization(organization_id)
    
    def get_by_category(self, category_id: int):
        return self.repository.get_by_category(category_id)
    
    def search(self, organization_id: int, query: str):
        return self.repository.search(organization_id, query)
    
    def create(self, data: dict):
        return self.repository.create(**data)
    
    def update(self, product_id: int, data: dict):
        product = self.repository.get_by_id(product_id)
        if not product:
            return None
        return self.repository.update(product, **data)
    
    def delete(self, product_id: int):
        product = self.repository.get_by_id(product_id)
        if not product:
            return False
        return self.repository.delete(product)


class CategoryService:
    """Servicio para Category"""
    
    def __init__(self):
        self.repository = CategoryRepository()
    
    def get_all(self):
        return self.repository.get_all()
    
    def get_by_id(self, category_id: int):
        return self.repository.get_by_id(category_id)
    
    def get_by_organization(self, organization_id: int):
        return self.repository.get_by_organization(organization_id)
    
    def create(self, data: dict):
        return self.repository.create(**data)
    
    def update(self, category_id: int, data: dict):
        category = self.repository.get_by_id(category_id)
        if not category:
            return None
        return self.repository.update(category, **data)
    
    def delete(self, category_id: int):
        category = self.repository.get_by_id(category_id)
        if not category:
            return False
        return self.repository.delete(category)
