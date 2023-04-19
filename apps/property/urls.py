from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.property.views import PropertyViewSet, ContractViewSet

app_name = 'property'

router = DefaultRouter()

router.register("property", PropertyViewSet, basename="property")
router.register("contract", ContractViewSet, basename="contract")

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += router.urls


