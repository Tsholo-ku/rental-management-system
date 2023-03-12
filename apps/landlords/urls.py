from django.urls import path
from .views import OwnerTenantList

app_name = 'landlord'
urlpatterns = [
    path('addtenant/', OwnerTenantList.as_view(), name='tenant_list'),
]
