from django.urls import path, include
from apps.landlords.views import LandlordViewSet
from rest_framework.routers import DefaultRouter

app_name = 'landlords'

router = DefaultRouter()

router.register("landlords", LandlordViewSet, basename="landlord")

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += router.urls