from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from apps.users.views import UserViewSet, UserRegistrationView

#Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()

router.register('apps.users', UserViewSet)
router = routers.DefaultRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('users/', include('apps.users.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('property/', include('apps.property.urls', namespace='property')),
    path('payment/', include('apps.payment.urls', namespace='payment')),
    path('invoices/', include('apps.invoices.urls', namespace='invoices')),
    path('landlord/', include('apps.landlords.urls', namespace='tenantlist')),
    path('tenant/', include('apps.tenants.urls', namespace='tenants'))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT) + router.urls
