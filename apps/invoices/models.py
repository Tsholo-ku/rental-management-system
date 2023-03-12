import datetime
import uuid
from django.db import models


class Invoice(models.Model):

    class Status(models.TextChoices):
        SENT = "SENT", "sent"
        PAID = "PAID", "paid"

    invoice_number = models.CharField(max_length=10, unique=True, editable=False)
    tenant_id = models.ForeignKey('tenants.Tenant', blank=True, null=True, on_delete=models.CASCADE)
    property_owner_id = models.ForeignKey('landlords.PropertyOwner', blank=True, null=True, on_delete=models.CASCADE)
    contract_id = models.ForeignKey('property.Contract', on_delete=models.CASCADE)
    invoice_amount = models.CharField(max_length=200, null=False, blank=False)
    notification_status = models.CharField(max_length=9, choices=Status.choices, default="ON REVIEW")
    invoice_status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # generate a new UUID with 4 digits
            uuid_int = uuid.uuid4().int & (1 << 16) - 1
            uuid_hex = format(uuid_int, 'x').zfill(4)
            self.invoice_number = 'INV-' + uuid_hex
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.tenant_id)
