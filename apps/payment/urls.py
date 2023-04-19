from django.urls import path, include
from apps.payment.views import PaymentViewSet
from rest_framework.routers import DefaultRouter

app_name = 'payment'

router = DefaultRouter()

router.register("payment", PaymentViewSet, basename="payment")

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += router.urls
