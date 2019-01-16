from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.contrib.rest_framework import TokenMatchesOASRequirements

from apps.products.models import Product, Category
from apps.web.serializers.products import ProductSerializer, CategorySerializer


class CategoryCreate(APIView, ProtectedResourceView):
    """
    A view to create `Categories`.

    * Requires authentication.
    * Only adminusers use.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "POST": [['product:write']]
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
                    # Creating category
                    category = Category()
                    category.name = request_data['name']

                    if 'description' in request_data:
                        category.description = request_data['description']

                    category.save()
                    return Response({"id": category.id}, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_409_CONFLICT)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CategoryList(APIView, ProtectedResourceView):
    """
    A view to list `Categories`.

    * Requires authentication.
    """
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "GET": [['product:read']]
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
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class CategoryUpdateDelete(APIView, ProtectedResourceView):
    """
    A view to update and delete a `Category`.

    * Requires authentication.
    * Only adminusers can use
    """

    serializer_class = CategorySerializer
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "PATCH": [['product:write']],
        "DELETE": [['product:write']]
    }

    def patch(self, request, pk, format=None):
        """
        Updates the category
        """
        try:
            category = Category.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.is_admin:

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                request_data = serializer.data  # Getting serialized data

                # Updating category
                if 'name' in request_data:
                    category.name = request_data['name']

                if 'description' in request_data:
                    category.description = request_data['description']

                category.save()
                return Response({"id": category.id}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, format=None):
        """
        Deletes the category
        """
        try:
            category = Category.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.is_admin:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ProductCreate(APIView, ProtectedResourceView):
    """
    A view to create `Products`.

    * Requires authentication.
    * Only adminusers create.
    """
    serializer_class = ProductSerializer
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "POST": [['product:write']]
    }

    def post(self, request, format=None):
        """
        Creates a new product
        """
        if request.user.is_admin:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():

                # Getting serialized data
                request_data = serializer.data
                if not Product.objects.filter(name=request_data['name']):
                    # Creating product
                    product = Product()
                    product.name = request_data['name']
                    product.category = Category.objects.get(
                        pk=request_data['category'])
                    product.purchase_price = request_data['purchase_price']
                    product.sale_price = request_data['sale_price']

                    if 'description' in request_data:
                        product.description = request_data['description']

                    product.save()
                    print(product)
                    return Response({"id": product.id}, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_409_CONFLICT)

            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class ProductList(APIView):
    """
    A view to list `Products`.

    * Do not requires authentication.
    """

    def get(self, request, format=None):
        """
        Retrieves a list of `Products`
        """
        # Getting categories
        products = Product.objects.filter()

        response = []
        for product in products:
            response.append({
                "id": product.id,
                "name": product.name,
                "category": product.category.name,
                "description": product.description,
                "sale_price": product.sale_price
            })
        return Response(response, status=status.HTTP_200_OK)


class ProductRetrieveUpdateDelete(APIView, ProtectedResourceView):
    """
    A view to retrieve, update and delete a `Product`.

    * Requires authentication.
    * Only adminusers can use
    """

    serializer_class = ProductSerializer
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "GET": [['product:read']],
        "PATCH": [['product:write']],
        "DELETE": [['product:write']]
    }

    def get(self, request, pk, format=None):
        """
        Retrieves a product
        """
        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.is_admin:
            # Parsing response
            response = {
                "id": product.id,
                "name": product.name,
                "category": product.category.name,
                "description": product.description,
                "purchase_price": product.purchase_price,
                "sale_price": product.sale_price,
                "created_at": product.created_at,
                "updated_at": product.updated_at
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, pk, format=None):
        """
        Updates the product
        """
        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.is_admin:

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                request_data = serializer.data  # Getting serialized data

                # Updating product
                if 'name' in request_data:
                    product.name = request_data['name']

                if 'category' in request_data:
                    product.category = Category.objects.get(
                        pk=request_data['category'])

                if 'description' in request_data:
                    product.description = request_data['description']

                if 'purchase_price' in request_data:
                    product.purchase_price = request_data['purchase_price']

                if 'sale_price' in request_data:
                    product.sale_price = request_data['sale_price']

                product.save()
                return Response({"id": product.id}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk, format=None):
        """
        Deletes the product
        """
        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.is_admin:
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
