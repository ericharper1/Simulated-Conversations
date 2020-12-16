from django.db import models


class TemplateResponse (models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True)
    completion_date = models.DateTimeField(default=None)
    student = models.ForeignKey('users.Student', related_name='template_responses', default=0, on_delete=models.DO_NOTHING)
    template = models.ForeignKey('conversation_templates.ConversationTemplate', default=0, related_name='template_responses', on_delete=models.CASCADE)
    assignment = models.ForeignKey('users.Assignment', default=0, related_name='template_responses', on_delete=models.CASCADE)
