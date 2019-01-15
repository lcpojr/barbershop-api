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
    address = AddressSerializer(many=False, required=False)
    phone = PhoneSerializer(many=False, required=False)
    document = DocumentSerializer(many=False, required=True)

    class Meta:
        model = Profile
        fields = (
            'full_name', 'mothers_name', 'fathers_name', 'birthdate',
            'email', 'password', 'address', 'phone', 'document',
        )


class UpdateSerializer(serializers.ModelSerializer):
    """
    Serializer to parse profile Json data on update
    """

    address = AddressSerializer(many=False, required=False)
    phone = PhoneSerializer(many=False, required=False)
    document = DocumentSerializer(many=False, required=False)

    class Meta:
        model = Profile
        fields = (
            'full_name', 'mothers_name', 'fathers_name',
            'birthdate', 'address', 'phone', 'document',
        )
