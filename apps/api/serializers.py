from rest_framework import serializers
from apps.person.models import Person, Address, Phone

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('country', 'uf', 'city', 'street', 'neighborhood', 'number', 'reference', 'zipcode', 'latitude', 'longitude')

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        fields = ('code', 'ddd', 'number')

class PersonSerializer(serializers.ModelSerializer):
    # User Fields
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(max_length=50, style={'input_type': 'password'})
    
    # FK Fields
    addresses = AddressSerializer(many=True, read_only=False, required=False)
    phones = PhoneSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'email', 'password','nickname', 'cpf', 'birth_date', 'addresses', 'phones')
