from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from apps.users.views import UserRegistrationView, UserViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register('users', UserViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="X Rentbook API",
        default_version="1.0",
        description="API Documentation for Rentbook"
    ),
    public=True,
    permission_classes=[],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include(router.urls)),
    path('users/', include('apps.users.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('property/', include('apps.property.urls', namespace='property')),
    path('payment/', include('apps.payment.urls', namespace='payment')),
    path('invoices/', include('apps.invoices.urls', namespace='invoices')),
    path('landlord/', include('apps.landlords.urls', namespace='tenantlist')),
    path('tenant/', include('apps.tenants.urls', namespace='tenants')),

    path('swagger/schema/', schema_view.with_ui('swagger',
         cache_timeout=0), name='swagger-schema'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT) + router.urls
