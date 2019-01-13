from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import User

class UserAdmin(admin.ModelAdmin):
    fields = ('email', 'date_joined', 'is_active', 'is_staff', 'is_superuser', 'user_permissions', 'groups')

admin.site.register(User, UserAdmin)
admin.site.register(Permission)