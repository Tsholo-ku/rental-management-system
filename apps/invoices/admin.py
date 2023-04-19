from django.contrib import admin
from apps.invoices.models import Invoice


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'invoice_amount', 'notification_status', 'invoice_status', 'created_at', 'updated_at']
    list_filter = ['notification_status', 'invoice_status', 'created_at']
    search_fields = ['invoice_number', 'tenant__name', 'landlord__name']

admin.site.register(Invoice, InvoiceAdmin)