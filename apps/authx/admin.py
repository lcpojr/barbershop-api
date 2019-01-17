from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Permission, Group

from .models import User
from .forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    list_display = ('email', 'created_at', 'is_active')
    list_filter = ('email', 'created_at', 'is_active')

    # The filds to be used in updates on User model.
    fieldsets = (
        ('Login', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_admin')}),
        ('Status', {'fields': ('is_active',)}),
    )

    # The fields to be used in inserts on User model.
    add_fieldsets = (
        ('Login', {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }
        ),
    )
    # Search and ordering
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Permission)
