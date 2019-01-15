"""
API URL Configuration for barbershop project.
It may contain api rest endpoints.
"""

from django.urls import include, path
from .controllers.person import PersonCreate, PersonRetrieveUpdate

urlpatterns = [
    # Person endpoints
    path('person/', PersonCreate.as_view(), name='person_create'),
    path('person/<uuid:pk>/', PersonRetrieveUpdate.as_view(),
         name='person_retrieve_update'),
]
