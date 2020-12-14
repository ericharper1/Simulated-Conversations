from django.db import models
from conversation_templates.models.conv_template import ConversationTemplate
from conversation_templates.models.template_response import TemplateResponse


class Student(CustomUser):
    template_response = models.ForeignKey(TemplateResponse, on_delete=models.CASCADE)
    available_templates = models.ManyToManyField(ConversationTemplate, related_name='')
    completed_templates = models.ManyToManyField(ConversationTemplate, related_name='')
    registered = models.BooleanField(default=False)

    def get_is_registered(self):
        return self.registered
