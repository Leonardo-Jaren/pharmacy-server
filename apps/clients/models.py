from django.db import models

# Create your models here.
class Client(models.Model):
    organization = models.ForeignKey('organization.Organization', null=False, blank=False, on_delete=models.CASCADE, related_name='clients')
    branch = models.ForeignKey('organization.Branch', null=True, blank=True, on_delete=models.SET_NULL, related_name='clients')
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    document_type = models.CharField(max_length=50, null=True, blank=True)
    document_number = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['organization', 'document_number'], name='uniq_org_client_document'),
        ]
        indexes = [
            models.Index(fields=['organization', 'document_number']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.document_number}"