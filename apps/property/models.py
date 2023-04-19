from django.db import models


class Property(models.Model):

    class Type(models.TextChoices):
        HOUSE = "HOUSE", "house"
        APARTMENT = "APARTMENT", "apartment"

    class Status(models.TextChoices):
        ON_REVIEW = "ON REVIEW", "on review"
        OPEN = "OPEN", "open"
        ON_HOLD = "ON HOLD", "on hold"
        BOOKED = "BOOKED", "booked"

    property_name = models.CharField(max_length=200, blank=False, null=False)
    landlord = models.ForeignKey("landlords.Landlord", blank=True, null=True, related_name='landlord', on_delete=models.CASCADE)
    type = models.CharField(max_length=9, choices=Type.choices, default="HOUSE")
    description = models.CharField(max_length=200, blank=False, null=False)
    address = models.CharField(max_length=200, blank=False, null=False)
    prop_images = models.FileField(upload_to='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=9, choices=Status.choices, default="ON REVIEW")

    def __str__(self):
        return self.property_name


class Contract(models.Model):

    class Payment_type(models.TextChoices):
        WEEKLY = "WEEKLY", "weekly"
        BIWEEKELY = "BIWEEKELY", "biweekely"
        MONTHLY = "MONTHLY", "monthly"
        YEARLY = "YEARLY", "yearly"

    property = models.ForeignKey(Property, blank=True, null=True, on_delete=models.CASCADE)
    tenant = models.ForeignKey("tenants.Tenant", blank=True, null=True, on_delete=models.CASCADE)
    landlord = models.ForeignKey("landlords.Landlord", blank=True, null=True, related_name='owner', on_delete=models.CASCADE)
    contract_starts = models.DateTimeField()
    contract_ends = models.DateTimeField()
    payment_type = models.CharField(max_length=20, choices=Payment_type.choices, default="MONTHLY")
    rental_amount = models.FloatField()
    contract_status = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # returns id of the contract
        return str(self.id)
