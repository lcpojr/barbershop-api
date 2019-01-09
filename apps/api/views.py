from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import PersonSerializer
from apps.person.behavior import create_person, create_address, create_phone

class CreatePerson(APIView):
    """
    A view to create a client `Person`.
    A `Person` object contains data of its user, address and phones.

    * Don't requires authentication.
    * Everyone can use this endpoint.
    """
    serializer_class = PersonSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            person = create_person(serializer.data)

            if 'addresses' in serializer.data:
                for address in serializer.data.addresses:
                    person.address.add(create_address(address))

            if 'phones' in serializer.data:
                for phone in serializer.data.phones:
                    person.phones.add(create_phone(phone))

            person.save()

            return Response({"id": person.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)