from django.db import models

# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False)
    tax_id = models.CharField(max_length=50, unique=True, null=False, default='RUC')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class CompanyCredentials(models.Model):
    organization = models.ForeignKey(Organization, null=False, blank=False, on_delete=models.PROTECT, related_name='credentials')
    sol_user = models.CharField(max_length=100, null=False, blank=False)
    sol_password = models.CharField(max_length=100, null=False, blank=False)
    sol_token = models.CharField(max_length=100, null=False, blank=False)
    certh_path = models.CharField(max_length=200, null=False, blank=False)
    certh_password = models.CharField(max_length=100, null=False, blank=False)
    is_production = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Credentials for {self.organization.name}"

class Branch(models.Model):
    organization = models.ForeignKey(Organization, null=False, blank=False, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=200, null=False, blank=False)
    address = models.CharField(max_length=300, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name} - {self.organization.name}"

#hace referencia a la serie de facturación por sucursal si es J10013 o B21391 sin que este se repita
class InvoiceSeries(models.Model):
    branch = models.ForeignKey(Branch, null=False, blank=False, on_delete=models.CASCADE, related_name='invoice_series')
    series = models.CharField(max_length=10, null=False, blank=False)
    current_number = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['branch', 'series'], name='uniq_branch_series'),
        ]
    
    def __str__(self):
        return f"Series {self.series} for {self.branch.name}"