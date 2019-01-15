"""
Django URL Configuration for barbershop project.
It may contain base configuration endpoints.
"""

from django.contrib import admin
from django.urls import include, path

from apps.web.controllers.profiles import ProfileListCreate, ProfileRetrieveUpdate

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Auth urls
    path('api/v1/auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Profiles urls
    path('api/v1/profiles/', ProfileListCreate.as_view(), name='profile_create'),
    path('api/v1/profiles/<uuid:pk>/', ProfileRetrieveUpdate.as_view(),
         name='profile_retrieve_update'),
]
