from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_active', 'is_researcher', 'is_staff')
    list_filter = ('email', 'is_active', 'is_researcher', 'is_staff')
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'password')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_researcher', 'is_staff')
        }),
    )
    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'is_active',
                   'is_researcher', 'is_staff')
    }), )
    search_fields = ('email', )
    ordering = ('email', )


admin.site.register(CustomUser, CustomUserAdmin)