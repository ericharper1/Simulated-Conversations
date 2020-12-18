from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from simcon_project.conversation_templates.models import *
from simcon_project.users.models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm


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


admin.site.register(ConversationTemplate)
admin.site.register(TemplateNode)
admin.site.register(TemplateNodeChoice)
admin.site.register(TemplateResponse)
admin.site.register(TemplateNodeResponse)
admin.site.register(Assignment)
admin.site.register(CustomUser)
admin.site.register(CustomUserManager)
admin.site.register(Researcher)
admin.site.register(Student)
admin.site.register(SubjectLabel)


