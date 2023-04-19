from rest_framework import serializers
from apps.tenants.models import Tenant


class TenantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tenant
        fields = ('id', 'user', 'property', 'landlord', 'address')
