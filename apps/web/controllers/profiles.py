from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.contrib.rest_framework.authentication import OAuth2Authentication
from oauth2_provider.contrib.rest_framework import TokenMatchesOASRequirements

from apps.authx.models import User
from apps.profiles.models import Profile
from apps.web.serializers.profiles import CreateSerializer, UpdateSerializer


class ProfileCreate(APIView):
    """
    A view to creates a `Profile`.

    * Do not requires authentication.
    """

    serializer_class = CreateSerializer

    def post(self, request, format=None):
        """
        Creates a new profile
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

                # Creating profile
                profile = Profile()
                profile.user = user
                profile.full_name = request_data['full_name']
                profile.birthdate = request_data['birthdate']

                if 'mothers_name' in request_data:
                    profile.mothers_name = request_data['mothers_name']

                if 'fathers_name' in request_data:
                    profile.fathers_name = request_data['fathers_name']

                if 'phone' in request_data:
                    profile.phone = request_data['phone']

                if 'address' in request_data:
                    profile.address = request_data['address']

                if 'document' in request_data:
                    profile.document = request_data['document']

                profile.save()
                return Response({"id": profile.id}, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileRetrieveUpdate(APIView, ProtectedResourceView):
    """
    A view to update a `Profile`.

    * Requires authentication.
    * Only staffusers and the profile itself can use
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
        Retrieves the profile data
        """
        profile = Profile.objects.get(pk=pk)
        if request.user.is_staff or request.user == profile.user:
            # Parsing response
            response = {
                "full_name": profile.full_name,
                "mothers_name": profile.mothers_name,
                "fathers_name": profile.fathers_name,
                "phone": profile.phone,
                "address": profile.address,
                "document": profile.document,
                "birthdate": profile.birthdate,
                "email": profile.user.email,
                "date_joined": profile.user.date_joined
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, pk, format=None):
        """
        Updates the profile data
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            request_data = serializer.data  # Getting serialized data
            profile = Profile.objects.get(pk=pk)  # Retrieving profile
            if request.user.is_staff or request.user == profile.user:
                # Updating profile
                if 'full_name' in request_data:
                    profile.full_name = request_data['full_name']

                if 'birthdate' in request_data:
                    profile.birthdate = request_data['birthdate']

                if 'mothers_name' in request_data:
                    profile.mothers_name = request_data['mothers_name']

                if 'fathers_name' in request_data:
                    profile.fathers_name = request_data['fathers_name']

                if 'phone' in request_data:
                    profile.phone = request_data['phone']

                if 'address' in request_data:
                    profile.address = request_data['address']

                if 'document' in request_data:
                    profile.document = request_data['document']

                profile.save()
                return Response({"id": profile.id}, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
