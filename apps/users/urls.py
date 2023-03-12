from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from apps.users.views import UserViewSet, LoginView
router = routers.DefaultRouter()
router.register('', UserViewSet, basename="users")

urlpatterns = [
    path('login/', LoginView.as_view(),name="login"),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),

]