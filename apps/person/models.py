import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField('Nickname', max_length=100, null=True)
    cpf = models.CharField('CPF', max_length=11, unique=True)
    birth_date = models.DateField('Date of birth')
     
    def __str__(self):
        return self.nickname

    def get_age(self):
        return timezone.now().year - self.birth_date.year

    def get_name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class Address(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    country = models.CharField('Country', max_length=30, default='Brazil')
    uf = models.CharField('UF', max_length=2)
    city = models.CharField('City', max_length=50)
    street = models.CharField('Street', max_length=100)    
    neighborhood = models.CharField('Neighborhood', max_length=100)
    number = models.CharField('Number', max_length=100)
    reference = models.TextField('Reference', max_length=100, null=True)
    zipcode = models.CharField('Zip code', max_length=8, null=True)
    latitude = models.FloatField('Latitude', null=True)
    longitude = models.FloatField('Longitude', null=True)

    def __str__(self):
        return '{}, {}, {}, {} - {}'.format(self.street, self.number, self.neighborhood, self.city, self.uf)

    def get_full_address(self):
        return self.__str__() + ', {} ({})'.format(self.country, self.zipcode)


class Phone(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    code = models.IntegerField(default=55)
    ddd = models.IntegerField()
    number = models.IntegerField()

    def __str__(self):
        return '+{} ({}) {}'.format(self.code, self.ddd, self.number)
    