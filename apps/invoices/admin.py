from django.contrib import admin
from .models import Invoice


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'tenant_id', 'property_owner_id', 'invoice_amount', 'notification_status', 'invoice_status', 'created_at', 'updated_at']
    list_filter = ['notification_status', 'invoice_status', 'created_at']
    search_fields = ['invoice_number', 'tenant_id__name', 'property_owner_id__name']

admin.site.register(Invoice, InvoiceAdmin)