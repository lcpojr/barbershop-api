"""
Django URL Configuration for barbershop project.
It may contain base configuration endpoints.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Oauth2
    path('api/v1/auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
