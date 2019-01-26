"""
Django URL Configuration for barbershop project.
It may contain base configuration endpoints.
"""

from django.contrib import admin
from django.urls import include, path

from apps.web.controllers import profiles, products, sales

urlpatterns = [
    # Django admin
    path('admin/', admin.site.urls),

    # Auth urls
    path('api/v1/auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # Profiles urls
    path('api/v1/profiles/', profiles.ProfileCreate.as_view(),
         name='profile_create'),
    path('api/v1/profiles/me', profiles.ProfileMe.as_view(),
         name='profile_me'),
    path('api/v1/profiles/list/', profiles.ProfileList.as_view(),
         name='profile_list'),
    path('api/v1/profiles/<uuid:pk>/', profiles.ProfileRetrieveUpdate.as_view(),
         name='profile_retrieve_update'),

    # Products urls
    path('api/v1/categories/', products.CategoryCreate.as_view(),
         name='category_create'),
    path('api/v1/categories/list/', products.CategoryList.as_view(),
         name='category_list'),
    path('api/v1/categories/<uuid:pk>/', products.CategoryUpdateDelete.as_view(),
         name='category_update_delete'),
    path('api/v1/products/', products.ProductCreate.as_view(),
         name='product_create'),
    path('api/v1/products/list/', products.ProductList.as_view(),
         name='product_list'),
    path('api/v1/products/<uuid:pk>/qrcode/', products.ProductQRCode.as_view(),
         name='product_qrcode'),
    path('api/v1/products/<uuid:pk>/', products.ProductRetrieveUpdateDelete.as_view(),
         name='product_retrieve_update_delete'),

    # Sale urls
    path('api/v1/sales/', sales.SaleCreate.as_view(),
         name='sale_create'),
    path('api/v1/sales/list/', sales.SaleList.as_view(),
         name='sale_list'),
    path('api/v1/sales/<uuid:pk>/', sales.SaleRetrieve.as_view(),
         name='sale_retrieve'),
    path('api/v1/sales/<uuid:pk>/products/', sales.SaleUpdateRemoveProduct.as_view(),
         name='sale_update_remove_products'),
    path('api/v1/sales/<uuid:pk>/close/', sales.SaleClose.as_view(),
         name='sale_update_status_wating'),
    path('api/v1/sales/<uuid:pk>/cancelate/', sales.SaleCancelate.as_view(),
         name='sale_update_status_canceled'),
    path('api/v1/sales/<uuid:pk>/pay/', sales.SalePay.as_view(),
         name='sale_update_status_payed'),
]
