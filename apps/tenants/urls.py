from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.tenants.views import TenantViewSet

app_name = 'tenants'

router = DefaultRouter()

router.register("tenants", TenantViewSet, basename="tenant")

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += router.urls
