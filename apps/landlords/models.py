from django.db import models
from django.contrib.auth import get_user_model
from apps.property.models import Property

# from tenants.models import Tenant

# Create your models here.
User = get_user_model()


class PropertyOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tenants = models.ManyToManyField('tenants.Tenant', blank=True, null=True, related_name='tenant')
    property = models.ManyToManyField(Property, blank=True, null=True, related_name='property')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contact_number = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.user)
