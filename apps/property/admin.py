from django.contrib import admin
from apps.property.models import Property, Contract


admin.site.register(Property)
admin.site.register(Contract)