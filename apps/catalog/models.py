from django.db import models

# Create your models here.
class Product(models.Model):
    organization = models.ForeignKey('organization.Organization', null=False, blank=False, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    name = models.CharField(max_length=200, null=False, blank=False)
    generic_name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    barcode = models.CharField(max_length=100, unique=False, null=False, blank=False)
    presentation = models.CharField(max_length=200, null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    stack_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['organization', 'barcode'], name='uniq_org_product_barcode'),
            models.CheckConstraint(condition=models.Q(base_price__gte=0), name='product_price_non_negative'),
        ]
        indexes = [
            models.Index(fields=['organization', 'barcode']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.organization.name}"
    
class Category(models.Model):
    organization = models.ForeignKey('organization.Organization', null=False, blank=False, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name} - {self.organization.name}"