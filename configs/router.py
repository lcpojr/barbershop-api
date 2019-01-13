"""
Django URL Configuration for barbershop project.
It may contain base configuration endpoints.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Auth urls
    path('auth/', include(('apps.authx.urls', 'authx'), namespace='auth')),

    # API
    path('api/v1/', include(('apps.api.urls', 'rest_api'), namespace='api')),
]