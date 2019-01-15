from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from oauth2_provider.contrib.rest_framework import TokenMatchesOASRequirements

from apps.authx.models import User
from apps.profiles.models import Person
from apps.profiles.serializers import CreateSerializer, UpdateSerializer


class PersonCreate(APIView):
    """
    A view to creates a `Person`.

    * Do not requires authentication.
    """

    serializer_class = CreateSerializer

    def post(self, request, format=None):
        """
        Creates a new person
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Getting serialized data
            request_data = serializer.data
            if not User.objects.filter(email=request_data['email']):
                # Creating user
                user = User()
                user.email = request_data['email']
                user.set_password(request_data['password'])
                user.save()

                # Creating person
                person = Person()
                person.user = user
                person.full_name = request_data['full_name']
                person.birthdate = request_data['birthdate']

                if 'mothers_name' in request_data:
                    person.mothers_name = request_data['mothers_name']

                if 'fathers_name' in request_data:
                    person.fathers_name = request_data['fathers_name']

                if 'phone' in request_data:
                    person.phone = request_data['phone']

                if 'address' in request_data:
                    person.address = request_data['address']

                if 'document' in request_data:
                    person.document = request_data['document']

                person.save()
                return Response({"id": person.id}, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonRetrieveUpdate(APIView, ProtectedResourceView):
    """
    A view to update a `Person`.

    * Requires authentication.
    * Only staffusers and the person itself can use
    """

    serializer_class = UpdateSerializer
    authentication_classes = (OAuth2Authentication,)
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "GET": [['profile:read']],
        "PATCH": [['profile:write']]
    }

    def get(self, request, pk, format=None):
        """
        Retrieves the person data
        """
        person = Person.objects.get(pk=pk)
        if request.user.is_staff or request.user == person.user:
            # Parsing response
            response = {
                "full_name": person.full_name,
                "mothers_name": person.mothers_name,
                "fathers_name": person.fathers_name,
                "phone": person.phone,
                "address": person.address,
                "document": person.document,
                "birthdate": person.birthdate,
                "email": person.user.email,
                "date_joined": person.user.date_joined
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, pk, format=None):
        """
        Updates the person data
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            request_data = serializer.data  # Getting serialized data
            person = Person.objects.get(pk=pk)  # Retrieving person
            if request.user.is_staff or request.user == person.user:
                # Updating person
                if 'full_name' in request_data:
                    person.full_name = request_data['full_name']

                if 'birthdate' in request_data:
                    person.birthdate = request_data['birthdate']

                if 'mothers_name' in request_data:
                    person.mothers_name = request_data['mothers_name']

                if 'fathers_name' in request_data:
                    person.fathers_name = request_data['fathers_name']

                if 'phone' in request_data:
                    person.phone = request_data['phone']

                if 'address' in request_data:
                    person.address = request_data['address']

                if 'document' in request_data:
                    person.document = request_data['document']

                person.save()
                return Response({"id": person.id}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
