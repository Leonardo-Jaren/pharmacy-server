from django.db import models

# Create your models here.
#lote de productos para controlar fechas de vencimiento
class Batch(models.Model):
    branch = models.ForeignKey('organization.Branch', null=False, blank=False, on_delete=models.CASCADE, related_name='batches')
    product = models.ForeignKey('catalog.Product', null=False, blank=False, on_delete=models.CASCADE, related_name='batches')
    code = models.CharField(max_length=100, null=False)
    manufacture_date = models.DateField(null=False)
    expiration_date = models.DateField(null=False)
    stock_quantity = models.IntegerField(default=0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['branch', 'product', 'code'], name='uniq_branch_product_batch'),
            models.CheckConstraint(condition=models.Q(stock_quantity__gte=0), name='batch_stock_non_negative'),
        ]
        indexes = [
            models.Index(fields=['branch', 'expiration_date']),
        ]
    
    def __str__(self):
        return f"{self.code} - {self.product.name} - {self.branch.name}"

# Movimiento de stock para los lotes de productos entre branches(sucursales)
class StockMovement(models.Model):
    batch = models.ForeignKey(Batch, null=False, blank=False, on_delete=models.CASCADE, related_name='stock_movements')
    movement_type = models.CharField(max_length=50, null=False, blank=False)  # e.g., 'dentro', 'fuera'
    quantity = models.IntegerField(null=False)
    reason = models.CharField(max_length=200, null=True, blank=True)
    quantity_before = models.IntegerField(null=False)
    quantity_after = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.movement_type} - {self.quantity} for Batch {self.batch.code}"