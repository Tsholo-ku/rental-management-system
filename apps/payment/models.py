from django.db import models
from django.db import models
from apps.property.models import Contract
from apps.tenants.models import Tenant
from apps.landlords.models import Landlord
from apps.invoices.models import Invoice


class Payment(models.Model):

    class Payment_method(models.TextChoices):
        CASH = "CASH", "cash"
        ONLINE = "ONLINE", "online"


    contract_id = models.ForeignKey(Contract, blank=True, null = True, on_delete=models.CASCADE)
    tenant_id = models.ForeignKey(Tenant, blank=True, null = True, on_delete=models.CASCADE)
    landlord_id = models.ForeignKey(Landlord, blank=True, null=True, on_delete=models.CASCADE)
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices = Payment_method.choices, default="CASH")
    payment_status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}/{}".format(self.contract_id,self.tenant_id)#returns contract id and tenant id in the admin pannel

