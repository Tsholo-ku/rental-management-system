from django.urls import path
from apps.invoices.views import InvoiceListView, InvoiceCreateView, InvoiceUpdateView, InvoiceDeleteView

app_name = 'invoices'

urlpatterns = [
    path('', InvoiceListView.as_view(), name='invoice-list'),
    path('create/', InvoiceCreateView.as_view(), name='invoice-create'),
    path('update/<int:pk>/', InvoiceUpdateView.as_view(), name='invoice-update'),
    path('delete/<int:pk>/', InvoiceDeleteView.as_view(), name='invoice-delete'),
]