from django.shortcuts import render
from django.db import transaction

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.contrib.rest_framework import TokenMatchesOASRequirements

from apps.profiles.models import Profile
from apps.products.models import Product
from apps.sales.models import Sale, ProductItem
from apps.web.serializers.sales import SaleCreateSerializer, SaleEditProductSerializer


class SaleCreate(APIView, ProtectedResourceView):
    """
    A view to create `Sales`.

    * Requires authentication.
    """
    serializer_class = SaleCreateSerializer
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "POST": [['sale:write']]
    }

    def post(self, request, format=None):
        """
        Creates a new sale
        """
        if request.user.is_staff or request.user == request.data['client']:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                # Getting serialized data
                request_data = serializer.data
                if not Sale.objects.filter(client=request_data['client'], status="open"):
                    try:
                        with transaction.atomic():

                            # Creating sale
                            sale = Sale()
                            sale.client = Profile.objects.get(
                                pk=request_data['client'])
                            sale.status = 'open'

                            if 'employe' in request_data:
                                sale.employe = Profile.objects.get(
                                    pk=request_data['employe'])

                            # Adding products
                            if 'products' in request_data:
                                for product in request_data['products']:
                                    product_item = ProductItem()
                                    product_item.item = Product.objects.get(
                                        pk=product['item'])
                                    product_item.quantity = product['quantity']
                                    product_item.save()

                                    sale.products.add(product_item)

                            sale.save()
                            return Response({"id": sale.id}, status=status.HTTP_201_CREATED)

                    except:
                        return Response({"type": "internal_server_erro"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"type": "sale_already_exist"}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({"type": "validation_error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class SaleList(APIView, ProtectedResourceView):
    """
    A view to list `Sales`.

    * Requires authentication.
    * Only staffusers can use.
    """
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "GET": [['sale:read']]
    }

    def get(self, request, format=None):
        """
        Retrieves a list of `Sales`
        """
        if request.user.is_staff:
            # Getting categories
            sales = Sale.objects.filter()

            response = []
            for sale in sales:
                response.append({
                    "id": sale.id,
                    "client": sale.client.full_name,
                    "total": sale.get_total(),
                    "status": sale.status,
                    "created_at": sale.created_at,
                    "updated_at": sale.updated_at
                })
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class SaleRetrieve(APIView, ProtectedResourceView):
    """
    A view to update and retrieve a `Sale`.

    * Requires authentication.
    * Only staffusers and the profile itself can use
    """
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "GET": [['sale:read']]
    }

    def get(self, request, pk, format=None):
        """
        Retrieves a profile
        """
        try:
            sale = Sale.objects.get(pk=pk)
        except:
            return Response({"type": "not_found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_staff or request.user == sale.client.user:
            # Parsing response
            products = []
            for product_item in sale.products.all():
                products.append({
                    "id": product_item.id,
                    "name": product_item.item.name,
                    "price": product_item.item.sale_price,
                    "quantity": product_item.quantity
                })

            response = {
                "id": sale.id,
                "client": sale.get_client_name(),
                "employe": sale.get_employe_name(),
                "products": products,
                "total": sale.get_total(),
                "status": sale.status,
                "created_at": sale.created_at,
                "updated_at": sale.updated_at,
                "total": sale.get_total()
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class SaleUpdateProduct(APIView, ProtectedResourceView):
    """
    A view to add product to the `Sale`.

    * Requires authentication.
    * Only staffusers and the profile itself can use
    """
    serializer_class = SaleEditProductSerializer
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "PATCH": [['sale:write']]
    }

    def patch(self, request, pk, format=None):
        """
        Retrieves a profile
        """
        try:
            sale = Sale.objects.get(pk=pk)
        except:
            return Response({"type": "not_found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_staff or request.user == sale.client.user:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                # Getting serialized data
                request_data = serializer.data
                try:
                    with transaction.atomic():

                        # Parsing itens
                        products = []
                        for value in request_data['products']:
                            # Searching product item
                            product_item = sale.products.filter(
                                item__pk=value['item']).first()

                            if product_item:
                                # Updating sale product item
                                product_item.quantity = value['quantity']
                                product_item.save()
                            else:
                                # Adding new sale product item
                                product_item = ProductItem()
                                product_item.item = Product.objects.get(
                                    pk=value['item'])
                                product_item.quantity = value['quantity']
                                product_item.save()

                            products.append(product_item)

                        sale.products.set(products)
                        sale.save()

                        return Response({"id": sale.id}, status=status.HTTP_200_OK)
                except:
                    return Response({"type": "internal_server_error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"type": "validation_error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
