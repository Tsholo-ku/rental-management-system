from rest_framework import serializers
from apps.landlords.models import Landlord

class LandlordSerializer(serializers.ModelSerializer):
   class Meta:
        model = Landlord
        fields = ('user', 'tenants', 'property','created_at', 'updated_at', 'contact_number')