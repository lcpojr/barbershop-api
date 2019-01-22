from django.db import transaction

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from oauth2_provider.views.generic import ProtectedResourceView
from oauth2_provider.contrib.rest_framework import TokenMatchesOASRequirements

from apps.authx.models import User
from apps.profiles.models import Profile
from apps.web.serializers.profiles import CreateSerializer, UpdateSerializer


class ProfileCreate(APIView):
    """
    A view to create a `Profile`.

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
                try:
                    with transaction.atomic():
                        # Creating user
                        user = User()
                        user.email = request_data['email']
                        user.set_password(request_data['password'])
                        user.save()

                        # Creating profile
                        profile = Profile()
                        profile.user = user
                        profile.full_name = request_data['full_name']
                        profile.documents = request_data['documents']

                        profile.save()
                        return Response({"id": profile.id}, status=status.HTTP_201_CREATED)
                except:
                    return Response({"type": "internal_server_error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"type": "profile_already_exist"}, status=status.HTTP_409_CONFLICT)

        else:
            return Response({"type": "validation_error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProfileList(APIView, ProtectedResourceView):
    """
    A view to list `Profiles`.

    * Requires authentication.
    * Only staffusers and adminusers can use
    """

    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "GET": [['profile:read']],
    }

    def get(self, request, format=None):
        """
        Retrieves a list of `Profiles`
        """
        if request.user.is_staff:
            # Getting profiles
            profiles = Profile.objects.filter()

            response = []
            for profile in profiles:
                response.append({
                    "id": profile.id,
                    "full_name": profile.full_name,
                    "email": profile.user.email,
                    "is_active": profile.user.is_active,
                })
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileRetrieveUpdate(APIView, ProtectedResourceView):
    """
    A view to update and retrieve a `Profile`.

    * Requires authentication.
    * Only staffusers and the profile itself can use
    """

    serializer_class = UpdateSerializer
    permission_classes = (TokenMatchesOASRequirements,)
    required_alternate_scopes = {
        "GET": [['profile:read']],
        "PATCH": [['profile:write']]
    }

    def get(self, request, pk, format=None):
        """
        Retrieves a profile
        """
        try:
            profile = Profile.objects.get(pk=pk)
        except:
            return Response({"type": "not_found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_staff or request.user == profile.user:
            # Parsing response
            response = {
                "id": profile.id,
                "full_name": profile.full_name,
                "mothers_name": profile.mothers_name,
                "fathers_name": profile.fathers_name,
                "phones": profile.phones,
                "addresses": profile.addresses,
                "documents": profile.documents,
                "birthdate": profile.birthdate,
                "email": profile.user.email,
                "created_at": profile.created_at,
                "updated_at": profile.created_at,
                "is_active": profile.user.is_active,
                "is_staff": profile.user.is_staff,
                "is_admin": profile.user.is_admin
            }
            return Response(response, status=status.HTTP_200_OK)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, pk, format=None):
        """
        Updates the profile
        """
        try:
            profile = Profile.objects.get(pk=pk)
        except:
            return Response({"type": "not_found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user.is_staff or request.user == profile.user:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                try:
                    # Getting serialized data
                    request_data = serializer.data
                    with transaction.atomic():

                        # Updating profile
                        if 'full_name' in request_data:
                            profile.full_name = request_data['full_name']

                        if 'birthdate' in request_data:
                            profile.birthdate = request_data['birthdate']

                        if 'mothers_name' in request_data:
                            profile.mothers_name = request_data['mothers_name']

                        if 'fathers_name' in request_data:
                            profile.fathers_name = request_data['fathers_name']

                        if 'phones' in request_data:
                            profile.phones = request_data['phones']

                        if 'addresses' in request_data:
                            profile.addresses = request_data['addresses']

                        if 'documents' in request_data:
                            profile.documents = request_data['documents']

                        profile.save()
                        return Response({"id": profile.id}, status=status.HTTP_200_OK)

                except:
                    return Response({"type": "internal_server_error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"type": "validation_error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"type": "unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
