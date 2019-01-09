from django.contrib import admin
from .models import Person, Address, Phone

admin.site.register(Person)
admin.site.register(Address)
admin.site.register(Phone)
