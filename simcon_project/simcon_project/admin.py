from django.contrib import admin
from django.apps import apps
from simcon_project.conversation_templates.models import *

admin.site.register(ConversationTemplate)
admin.site.register(TemplateNode)
admin.site.register(TemplateNodeChoice)
admin.site.register(TemplateResponse)
admin.site.register(TemplateNodeResponse)

