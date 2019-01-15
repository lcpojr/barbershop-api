"""
API URL Configuration for barbershop project.
It may contain api rest endpoints.
"""

from django.urls import include, path
from .controllers.profiles import ProfileCreate, ProfileRetrieveUpdate

urlpatterns = [
    # Profile endpoints
    path('profiles/', ProfileCreate.as_view(), name='profile_create'),
    path('profiles/<uuid:pk>/', ProfileRetrieveUpdate.as_view(),
         name='profile_retrieve_update'),
]
