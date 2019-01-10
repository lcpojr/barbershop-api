from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    fields = ('email', 'date_joined', 'is_active', 'is_staff', 'is_superuser')

admin.site.register(User, UserAdmin)