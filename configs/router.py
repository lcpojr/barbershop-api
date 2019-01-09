"""
Django URL Configuration for barbershop project.
It may contain base configuration endpoints.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Custom urls
    path('api/v1/', include('apps.api.urls', namespace='api'))
]
