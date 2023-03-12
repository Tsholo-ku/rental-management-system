from rest_framework import serializers
from .models import Property
from .models import Contract


class PropertySerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Property.Status.choices)
    type = serializers.ChoiceField(choices=Property.Type.choices)

    class Meta:
        model = Property
        fields = ('id', 'property_name', 'type',
                  'description', 'address', 'status',)

    def validate_type(self, type):
        # custom validation
        if type != "HOUSE" and type != "APARTMENT":
            raise serializers.ValidationError("Invalid property type")
        return type

    def validate_status(self, status):
        if status != "ON REVIEW" and status != "OPEN" and status != "ON HOLD" and status != "BOOKED":
            raise serializers.ValidationError("Invalid status")
        return status


class ContractSerializer(serializers.ModelSerializer):
    payment_type = serializers.ChoiceField(
        choices=Contract.Payment_type.choices)
    tenant_name = serializers.CharField(
        source="tenant.user.username", read_only=True)
    property_name = serializers.CharField(
        source="property.property_name", read_only=True)

    class Meta:
        model = Contract
        fields = ['property_name', 'tenant_name', 'owner', 'contract_starts', 'contract_ends',
                  'payment_type', 'payment_amount', 'contract_status', 'created_at', 'updated_at']

    # def validate_contract_status(self, value):
    #     print('here')
    #     return value
    # def validate_Payment_type(self, payment_type):
    #     if payment_type != "WEEKLY" and payment_type != "BIWEEKELY" and payment_type != "MONTHLY" and payment_type != "YEARLY":
    #         raise serializers.ValidationError("Invalid payment type")
    #     return payment_type
