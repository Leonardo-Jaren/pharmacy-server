from django.db import models

# Create your models here.
class CashOperation(models.Model):
    cash_shift = models.ForeignKey('CashShift', null=False, blank=False, on_delete=models.CASCADE, related_name='operations')
    operation_type = models.CharField(max_length=50, null=False, blank=False)  # e.g., 'deposit', 'withdrawal'
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    description = models.TextField(null=True, blank=True)
    receipt_image = models.ImageField(upload_to='cash_operations/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.operation_type} - {self.amount} for Shift {self.cash_shift.id}"

class CashShift(models.Model):
    user = models.ForeignKey('users.User', null=True, blank=True, on_delete=models.SET_NULL, related_name='cash_shifts')
    branch = models.ForeignKey('organization.Branch', null=False, blank=False, on_delete=models.PROTECT, related_name='cash_shifts')
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    total_sales_cash = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        status = "Closed" if self.is_closed else "Open"
        return f"Cash Shift {self.id} - {status} for {self.user.username}"