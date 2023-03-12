from rest_framework import serializers
from .models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    notification_status = serializers.ChoiceField(choices=Invoice.Status.choices)
    
    class Meta:
        model = Invoice
        fields = ('invoice_number', 'tenant_id','property_owner_id', 'invoice_amount','notification_status','invoice_status')

    def validate_type(self, notification_status):
        # custom validation
        if notification_status != "PAID" and notification_status != "SENT":
            raise serializers.ValidationError("Invalid property type")
        return notification_status
