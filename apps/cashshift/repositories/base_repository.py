from abc import ABC
from typing import Optional, Any
from django.db.models import QuerySet
from django.core.paginator import Paginator


class BaseRepository(ABC):
    """Repositorio base con operaciones comunes"""
    
    def __init__(self, model_class):
        self.model_class = model_class
    
    def get_all(self) -> QuerySet:
        return self.model_class.objects.all()
    
    def get_by_id(self, id: int) -> Optional[Any]:
        try:
            return self.model_class.objects.get(id=id)
        except self.model_class.DoesNotExist:
            return None
    
    def create(self, **kwargs) -> Any:
        return self.model_class.objects.create(**kwargs)
    
    def update(self, instance: Any, **kwargs) -> Any:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
        return instance
    
    def delete(self, instance: Any) -> bool:
        instance.delete()
        return True
    
    def paginate(self, queryset: QuerySet, page: int, per_page: int = 10):
        paginator = Paginator(queryset, per_page)
        return paginator.get_page(page)
