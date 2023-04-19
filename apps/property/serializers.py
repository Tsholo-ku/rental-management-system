from rest_framework import serializers
from apps.property.models import Property
from apps.payment.models import Contract


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
    payment_type = serializers.ChoiceField(choices=Contract.Payment_type.choices)
    tenant_name = serializers.CharField(source="tenant.user.username", read_only=True)
    property_name = serializers.CharField(source="property.property_name", read_only=True)

    class Meta:
        model = Contract
        fields = ('id', 'tenant_name', 'property_name', 'tenant', 'property', 'contract_starts', 'contract_ends',
                  'payment_type', 'rental_amount', 'contract_status', 'created_at', 'updated_at')


class ContractImageUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contract
        fields = ['id', 'contract_image']