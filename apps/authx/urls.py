"""
Auth URL Configuration for barbershop project.
It may contain oauth and allauth configuration endpoints.
"""

from django.urls import include, path
import oauth2_provider.views as oauth2_views
from django.conf import settings

# OAuth2 provider endpoints
oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        path('applications/', oauth2_views.ApplicationList.as_view(), name="list"),
        path('applications/register/', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        path('applications/(?P<pk>\d+)/', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        path('applications/(?P<pk>\d+)/delete/', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        path('applications/(?P<pk>\d+)/update/', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        path('authorized-tokens/', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        path('authorized-tokens/(?P<pk>\d+)/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(), name="authorized-token-delete"),
    ]

app_name = 'authx'
urlpatterns = [
    # OAuth 2 endpoints:
    path('', include(oauth2_endpoint_views, namespace="oauth2_provider")),
]