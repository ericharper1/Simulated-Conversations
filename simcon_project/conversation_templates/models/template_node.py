from django.db import models


class TemplateNode (models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True)
    description = models.CharField(max_length=4000)
    video_url = models.URLField(max_length=100)
    start = models.BooleanField(default=False)
    terminal = models.BooleanField(default=False)
    parent_template = models.ForeignKey('conversation_templates.ConversationTemplate', default=0, related_name='template_nodes', on_delete=models.CASCADE)
