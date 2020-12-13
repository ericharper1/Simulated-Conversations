from django.db import models

class TemplateNode (models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True)
    description = models.CharField(max_length=4000)
    video_url = models.CharField(max_length=100)
    terminal = models.BooleanField(default=False)
    choices = models.ManyToManyField(TemplateNodeChoice, related_name='template_node')