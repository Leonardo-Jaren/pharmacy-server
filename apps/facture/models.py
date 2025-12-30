from django.db import models

# Create your models here.
class ElectronicDocumentType(models.Model):
    TYPE_CHOICES = [
        ('invoice', 'Invoice'),
        ('credit_note', 'Credit Note'),
        ('debit_note', 'Debit Note'),
    ]
    
    name = models.CharField(max_length=100, choices=TYPE_CHOICES, unique=True, null=False)
    sale = models.ForeignKey('sales.Sale', null=False, blank=False, on_delete=models.CASCADE, related_name='electronic_documents')
    series = models.CharField(max_length=10, null=False, blank=False)
    correlative = models.IntegerField(null=False)
    xml_link = models.URLField(max_length=300, null=True, blank=True)
    cdr_link = models.URLField(max_length=300, null=True, blank=True)
    sunat_status = models.CharField(max_length=100, null=True, blank=True)
    hash_code = models.CharField(max_length=200, null=True, blank=True)
    qr_data = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.get_name_display()