"""
Django URL Configuration for barbershop project.
It may contain base configuration endpoints.
"""

from django.contrib import admin
from django.urls import include, path

from apps.web.controllers import profiles, products

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Auth urls
    path('api/v1/auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Profiles urls
    path('api/v1/profiles/', profiles.ProfileCreate.as_view(),
         name='profile_create'),
    path('api/v1/profiles/list', profiles.ProfileList.as_view(),
         name='profile_list'),
    path('api/v1/profiles/<uuid:pk>/', profiles.ProfileRetrieveUpdate.as_view(),
         name='profile_retrieve_update'),

    # Products urls
    path('api/v1/categories/', products.CategoryCreate.as_view(),
         name='category_create'),
    path('api/v1/categories/list', products.CategoryList.as_view(),
         name='category_list'),
    path('api/v1/categories/<uuid:pk>/', products.CategoryUpdateDelete.as_view(),
         name='category_update_delete'),
    path('api/v1/products/', products.ProductCreate.as_view(),
         name='product_create'),
    path('api/v1/products/list', products.ProductList.as_view(),
         name='product_list'),
    path('api/v1/products/<uuid:pk>/', products.ProductRetrieveUpdateDelete.as_view(),
         name='product_retrieve_update_delete'),
]
