from django.db import models

# Create your models here.
class Sale(models.Model):
    branch = models.ForeignKey('organization.Branch', null=False, blank=False, on_delete=models.PROTECT, related_name='sales')
    cash_shift = models.ForeignKey('cashshift.CashShift', null=False, blank=False, on_delete=models.PROTECT, related_name='sales')
    user = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='sales')
    client = models.ForeignKey('clients.Client', null=True, blank=True, on_delete=models.SET_NULL, related_name='sales')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)
    status = models.CharField(max_length=50, null=False, blank=False)  # e.g., 'completed', 'pending', 'canceled'
    invoice_number = models.CharField(max_length=100, null=False) #facturación
    document_type = models.CharField(max_length=50, null=False, blank=False)  # e.g., 'Boleta', 'Factura'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['branch', 'document_type', 'invoice_number'], name='uniq_branch_doctype_invoice'),
        ]
        indexes = [
            models.Index(fields=['branch', 'created_at']),
            models.Index(fields=['client', 'created_at']),
        ]
    
    def __str__(self):
        return f"Sale {self.invoice_number} - {self.status} - {self.total_amount}"

class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, null=False, blank=False, on_delete=models.CASCADE, related_name='details')
    batch = models.ForeignKey('inventory.Batch', null=False, blank=False, on_delete=models.CASCADE, related_name='sale_details')
    product = models.ForeignKey('catalog.Product', null=False, blank=False, on_delete=models.CASCADE, related_name='sale_details')
    quantity = models.IntegerField(null=False)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    igv_type = models.CharField(max_length=50, null=False, blank=False)  # e.g., 'taxed', 'exempt', 'unaffected'
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Detail for Sale {self.sale.invoice_number} - Product {self.product.name}"

class SalePayment(models.Model):
    sale = models.ForeignKey(Sale, null=False, blank=False, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=50, null=False, blank=False)  # e.g., 'cash', 'credit_card', 'mobile_payment'
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Payment of {self.amount} for Sale {self.sale.invoice_number} via {self.payment_method}"