from django.urls import path, include
from apps.invoices.views import InvoiceViewSet
from rest_framework.routers import DefaultRouter

app_name = 'invoices'

router = DefaultRouter()

router.register("invoices", InvoiceViewSet, basename="invoice")

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += router.urls