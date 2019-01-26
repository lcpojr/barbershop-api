from rest_framework import serializers

from apps.profiles.models import Profile


class AddressSerializer(serializers.Serializer):
    """
    Serializer to parse address Json data
    """
    uf = serializers.CharField(max_length=2)
    city = serializers.CharField(max_length=50)
    street = serializers.CharField(max_length=50)
    neighborhood = serializers.CharField(max_length=50)
    number = serializers.CharField(max_length=20)
    reference = serializers.CharField(
        max_length=200, style={'base_template': 'textarea.html'}, required=False)
    zipcode = serializers.IntegerField(required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)


class PhoneSerializer(serializers.Serializer):
    """
    Serializer to parse phone Json data
    """
    ddd = serializers.IntegerField()
    number = serializers.IntegerField()


class DocumentSerializer(serializers.Serializer):
    """
    Serializer to parse document Json data
    """
    type = serializers.CharField(max_length=10)
    number = serializers.CharField(max_length=50)


class CreateSerializer(serializers.ModelSerializer):
    """
    Serializer to parse profile Json data on creation
    """

    # User filds
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(
        max_length=50, style={'input_type': 'password'})

    # Profile extra fields
    documents = DocumentSerializer(many=True, required=True)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'password', 'documents')


class UpdateSerializer(serializers.ModelSerializer):
    """
    Serializer to parse profile Json data on update
    """

    addresses = AddressSerializer(many=True, required=False)
    phones = PhoneSerializer(many=True, required=False)
    documents = DocumentSerializer(many=True, required=False)
    is_staff = serializers.BooleanField(required=False)
    is_admin = serializers.BooleanField(required=False)
    is_active = serializers.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = (
            'first_name', 'last_name', 'mothers_name', 'fathers_name',
            'birthdate', 'addresses', 'phones', 'documents', 'is_staff',
            'is_admin', 'is_active'
        )
