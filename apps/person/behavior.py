"""
A behavior module to perform actions on tables like
create, update, get, delete data.
"""

from django.contrib.auth.models import User
from .models import Person, Address, Phone

def create_person(data):
    """
    Creates a new `Person` with its `User`
    """
    person = Person()
    person.user = create_user(data)
    person.nickname = data['nickname']
    person.cpf = data['cpf']
    person.birth_date = data['birth_date']
    person.save()
    
    return person

def create_user(data):
    """
    Creates a new `User`
    """
    user = User.objects.create_user(data['email'], data['email'], data['password'])
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.save()

    return user

def create_address(data):
    """
    Creates a new `Address`
    """
    address = Address()
    address.country = data['country']
    address.uf = data['uf']
    address.city = data['city']
    address.street = data['street']
    address.neighborhood = data['neighborhood']
    address.number = data['number']
    address.reference = data['reference']
    address.zipcode = data['zipcode']
    address.latitude = data['latitude']
    address.longitude = data['longitude']
    address.save()

    return address

def create_phone(data):
    """
    Creates a new `Phone`
    """
    phone = Phone()
    phone.code = data['code']
    phone.ddd = data['ddd']
    phone.number = data['number']
    phone.save()

    return phone
