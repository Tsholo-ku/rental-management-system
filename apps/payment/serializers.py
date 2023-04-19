from rest_framework import serializers
from apps.property.serializers import ContractSerializer
from apps.payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ['contract_id','tenant_id','property_owner_id','payment_amount', 'payment_method','payment_status','created_at','updated_at',]

    def get_contract(self, obj):
        # serialize Contract object to dictionary
        contract = ContractSerializer(obj.contract).data
        return contract

    def validate_Payment_method(self,payment_method):
        if payment_method != "CASH" and payment_method != "ONLINE":
            raise serializers.ValidationError("Invalid Payment Method")
        return payment_method