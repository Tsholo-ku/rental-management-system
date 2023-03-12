from rest_framework import serializers
from .models import PropertyOwner

class PropertyOwnerSerializer(serializers.ModelSerializer):
   class Meta:
        model = PropertyOwner
        fields = ('user', 'tenants', 'property','created_at', 'updated_at', 'contact_number')