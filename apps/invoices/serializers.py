from rest_framework import serializers
from apps.invoices.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('id', 'invoice_number', 'tenant','landlord', 'invoice_amount','notification_status','invoice_status')
