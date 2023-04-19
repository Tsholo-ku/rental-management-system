from django.db import models
from apps.property.models import Property
from django.contrib.auth import get_user_model


User = get_user_model()


class Tenant(models.Model):

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.CASCADE, )
    landlord = models.ManyToManyField('landlords.Landlord', blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.id)
