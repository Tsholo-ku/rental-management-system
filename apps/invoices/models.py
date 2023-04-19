import datetime
import uuid
from django.db import models


class Invoice(models.Model):

    class Status(models.TextChoices):
        SENT = "SENT", "sent"
        PAID = "PAID", "paid"
        ON_REVIEW = "ON REVIEW", "on review"

    payment_date = models.DateField(default=datetime.date.today)
    invoice_number = models.CharField(max_length=10, unique=True, editable=False)
    tenant = models.OneToOneField('tenants.Tenant', blank=True, null=True, on_delete=models.CASCADE)
    landlord = models.ForeignKey('landlords.Landlord', blank=True, null=True, on_delete=models.CASCADE)
    contract_id = models.ForeignKey('property.Contract', null=True, blank=True, on_delete=models.CASCADE) 
    invoice_amount = models.FloatField(default=0)
    notification_status = models.CharField(max_length=9, choices=Status.choices, default="ON REVIEW")
    invoice_status = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # generate a new UUID with 4 digits
            uuid_int = uuid.uuid4().int & (1 << 16) - 1
            uuid_hex = format(uuid_int, 'x').zfill(4)
            self.invoice_number = str('INV-' + uuid_hex)
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.tenant)
