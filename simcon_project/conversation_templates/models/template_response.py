from django.db import models
from django.utils import timezone


class TemplateResponse (models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True)
    completion_date = models.DateTimeField(default=timezone.now)
    student = models.ForeignKey(users.Student, related_name='template_response')
    template = models.ForeignKey(ConversationTemplate, related_name='template_response')