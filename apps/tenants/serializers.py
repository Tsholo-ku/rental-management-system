from rest_framework import serializers
from .models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    contact_number = serializers.CharField(
        source="user.contact_number", read_only=True)
    full_name = serializers.CharField(
        source="user.full_name", read_only=True)

    class Meta:
        model = Tenant
        fields = ('id', 'full_name', 'username',
                  'address', 'contact_number')
