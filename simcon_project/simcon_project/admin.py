from django.contrib import admin
from django.apps import apps
from simcon_project.conversation_templates.models import *
from simcon_project.users.models import *

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


