from django.shortcuts import render
from django.views.generic import View
from django.db import transaction

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.contrib.rest_framework import TokenMatchesOASRequirements

from apps.services.models import Service, Category
from apps.web.serializers.services import ServiceSerializer, CategorySerializer


class CategoryCreate(APIView, ProtectedResourceView):
    """
    A view to create `Categories`.

    * Requires authentication.
    * Only adminusers use.
    """
    serializer_class = CategorySerializer
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "POST": [['service:write']]
    }

    def post(self, request, format=None):
        """
        Creates a new category
        """
        if request.user.is_admin:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                # Getting serialized data
                request_data = serializer.data
                if not Category.objects.filter(name=request_data['name']):
                    try:
                        with transaction.atomic():

                            # Creating category
                            category = Category()
                            category.name = request_data['name']

                            if 'description' in request_data and request_data['description']:
                                category.description = request_data['description']

                            category.save()
                            return Response({"id": category.id}, status=status.HTTP_201_CREATED)

                    except Exception as e:
                        return Response({"type": "internal_server_error", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"type": "category_already_exist"}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({"type": "validation_error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class CategoryList(APIView, ProtectedResourceView):
    """
    A view to list `Categories`.

    * Requires authentication.
    """
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "GET": [['service:read']]
    }

    def get(self, request, format=None):
        """
        Retrieves a list of `Categories`
        """
        if request.user.is_admin:
            # Getting categories
            categories = Category.objects.filter()

            response = []
            for category in categories:
                response.append({
                    "id": category.id,
                    "name": category.name,
                    "description": category.description,
                    "created_at": category.created_at,
                    "updated_at": category.updated_at,
                })
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class CategoryUpdateDelete(APIView, ProtectedResourceView):
    """
    A view to update and delete a `Category`.

    * Requires authentication.
    * Only adminusers can use
    """

    serializer_class = CategorySerializer
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "PATCH": [['service:write']],
        "DELETE": [['service:write']]
    }

    def patch(self, request, pk, format=None):
        """
        Updates the category
        """
        try:
            category = Category.objects.get(pk=pk)
        except:
            return Response({"type": "not_found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_admin:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                try:
                    # Getting serialized data
                    request_data = serializer.data
                    with transaction.atomic():

                        # Updating category
                        if 'name' in request_data and request_data['name']:
                            category.name = request_data['name']

                        if 'description' in request_data and request_data['description']:
                            category.description = request_data['description']

                        category.save()
                        return Response({"id": category.id}, status=status.HTTP_200_OK)

                except Exception as e:
                    return Response({"type": "internal_server_error", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"type": "validation_error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, format=None):
        """
        Deletes the category
        """
        try:
            category = Category.objects.get(pk=pk)
        except:
            return Response({"type": "not_found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_admin:
            try:
                with transaction.atomic():

                    # Deleting category
                    category.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)

            except:
                return Response({"type": "internal_server_error", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class ServiceCreate(APIView, ProtectedResourceView):
    """
    A view to create `Services`.

    * Requires authentication.
    * Only adminusers create.
    """
    serializer_class = ServiceSerializer
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "POST": [['service:write']]
    }

    def post(self, request, format=None):
        """
        Creates a new service
        """
        if request.user.is_admin:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                # Getting serialized data
                request_data = serializer.data
                if not Service.objects.filter(name=request_data['name']):
                    try:
                        with transaction.atomic():

                            # Creating service
                            service = Service()
                            service.name = request_data['name']
                            service.category = Category.objects.get(
                                pk=request_data['category'])
                            service.cost_price = request_data['cost_price']
                            service.sale_price = request_data['sale_price']

                            if 'description' in request_data and request_data['description']:
                                service.description = request_data['description']

                            service.save()
                            return Response({"id": service.id}, status=status.HTTP_201_CREATED)

                    except Exception as e:
                        return Response({"type": "internal_server_error", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({"type": "service_already_exist"}, status=status.HTTP_409_CONFLICT)
            else:
                return Response({"type": "validation_error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class ServiceList(APIView):
    """
    A view to list `Services`.

    * Requires authentication.
    """

    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "GET": [['service:read']]
    }

    def get(self, request, format=None):
        """
        Retrieves a list of `Services`
        """
        # Getting categories
        services = Service.objects.filter()

        response = []
        for service in services:
            response.append({
                "id": service.id,
                "name": service.name,
                "category": service.category.name,
                "description": service.description,
                "sale_price": service.sale_price
            })
        return Response(response, status=status.HTTP_200_OK)


class ServiceQRCode(View):
    """
    A view to get a `Service` QRCode.

    * Requires authentication.
    * Only staffusers and adminusers can use.
    * It will render an html with the code.
    """

    def get(self, request, pk, format=None):
        """
        Retrieves a `Service` and show its QRCode.
        """
        try:
            service = Service.objects.get(pk=pk)
        except:
            return render(request, 'errors/404_qrcode.html')

        return render(request, 'service_qrcode.html', {"service": service})


class ServiceRetrieveUpdateDelete(APIView, ProtectedResourceView):
    """
    A view to retrieve, update and delete a `Service`.

    * Requires authentication.
    * Only adminusers can use
    """

    serializer_class = ServiceSerializer
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "GET": [['service:read']],
        "PATCH": [['service:write']],
        "DELETE": [['service:write']]
    }

    def get(self, request, pk, format=None):
        """
        Retrieves a service
        """
        try:
            service = Service.objects.get(pk=pk)
        except:
            return Response({"type": "not_found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_admin:
            # Parsing response
            response = {
                "id": service.id,
                "name": service.name,
                "category": service.category.name,
                "description": service.description,
                "cost_price": service.cost_price,
                "sale_price": service.sale_price,
                "created_at": service.created_at,
                "updated_at": service.updated_at
            }
            return Response(response, status=status.HTTP_200_OK)
        elif request.user:
            # Parsing response
            response = {
                "id": service.id,
                "name": service.name,
                "category": service.category.name,
                "description": service.description,
                "sale_price": service.sale_price
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, pk, format=None):
        """
        Updates the service
        """
        try:
            service = Service.objects.get(pk=pk)
        except:
            return Response({"type": "not_found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_admin:

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                # Getting serialized data
                request_data = serializer.data
                try:
                    with transaction.atomic():

                        # Updating service
                        if 'name' in request_data and request_data['name']:
                            service.name = request_data['name']

                        if 'category' in request_data and request_data['category']:
                            service.category = Category.objects.get(
                                pk=request_data['category'])

                        if 'description' in request_data and request_data['description']:
                            service.description = request_data['description']

                        if 'cost_price' in request_data and request_data['cost_price']:
                            service.cost_price = request_data['cost_price']

                        if 'sale_price' in request_data and request_data['sale_price']:
                            service.sale_price = request_data['sale_price']

                        service.save()
                        return Response({"id": service.id}, status=status.HTTP_200_OK)

                except Exception as e:
                    return Response({"type": "internal_server_error", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"type": "validation_error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, format=None):
        """
        Deletes the service
        """
        try:
            service = Service.objects.get(pk=pk)
        except:
            return Response({"type": "not_found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_admin:
            try:
                with transaction.atomic():

                    # Deleting service
                    service.delete()
                    return Response(status=status.HTTP_204_NO_CONTENT)

            except Exception as e:
                return Response({"type": "internal_server_error", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
