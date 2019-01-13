"""
Auth URL Configuration for barbershop project.
It may contain oauth and allauth configuration endpoints.
"""

from django.urls import include, path

urlpatterns = [
    # OAuth endpoints
    path('o/', include(('oauth2_provider.urls', 'authx'), namespace='oauth2_provider')),

    # Allauth endpoints
    path('accounts/', include(('allauth.urls', 'authx'), namespace='allauth_provider')),
]