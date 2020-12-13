from django.db import models
from .custom_user import CustomUser
from conversation_templates.models.template import Template
from conversation_templates.models.template_response import TemplateResponse

class Student(CustomUser):
    template_response = models.ForeignKey(TemplateResponse, on_delete=models.CASCADE)
    available_templates = models.ManyToMany(Template, related_name='')
    completed_templates = models.ManyToMany(Template, related_name='')
    registered = models.BooleanField(default=False)

    def get_is_registered(self):
        return self.registered