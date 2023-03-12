from django.urls import path
from .views import TenantListView, TenantRemoveView

app_name = 'tenants'
urlpatterns = [
    path('list/', TenantListView.as_view(), name='tenant_list'),
    path('delete/<int:pk>/', TenantRemoveView.as_view(), name='tenant-delete'),

]