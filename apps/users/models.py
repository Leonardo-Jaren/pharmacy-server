from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Role(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('pharmacist', 'Pharmacist'),
        ('cashier', 'Cashier'),
        ('customer', 'Customer'),
    ]
    
    name = models.CharField(max_length=100, choices=ROLE_CHOICES, unique=True, null=False)
    
    def __str__(self):
        return self.get_name_display()

class User(AbstractUser):
    # username/email/password vienen de AbstractUser (password con hashing)
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    branch = models.ForeignKey('organization.Branch', null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    id_google = models.CharField(max_length=200, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username