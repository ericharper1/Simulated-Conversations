from django.db import models
import uuid


class TemplateResponse(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    completion_date = models.DateTimeField(default=None)
    student = models.ForeignKey('users.Student', related_name='template_responses', default=0, on_delete=models.CASCADE)
    template = models.ForeignKey('conversation_templates.ConversationTemplate', default=0,
                                 related_name='template_responses', on_delete=models.CASCADE)
    assignment = models.ForeignKey('users.Assignment', default=0, related_name='template_responses',
                                   on_delete=models.CASCADE)
    feedback = models.CharField(max_length=1000, default='No feedback')
