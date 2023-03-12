from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    payment_method = serializers.ChoiceField(
        choices=Payment.Payment_method.choices)

    class Meta:
        model = Payment
        fields = ['contract_id','tenant_id','property_owner_id','payment_method','payment_status','created_at','updated_at']

    def validate_Payment_method(self,payment_method):
        if payment_method != "CASH" and payment_method != "ONLINE":
            raise serializers.ValidationError("Invalid Payment Method")
        return payment_method