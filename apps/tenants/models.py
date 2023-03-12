import datetime
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
class Tenant(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_no = models.IntegerField(default=None, unique=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=100, null=False, blank=False, unique=True)
    contact_no = models.IntegerField(default=None, unique=True)
    landlord = models.OneToOneField('landlords.PropertyOwner', on_delete=models.CASCADE, related_name='landlord')
    
    def __str__(self):
        return self.email

    
    