from django.db import models
from .template_node import TemplateNode


class TemplateNodeResponse (models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True)
    transcription = models.CharField(max_length=1000)
    template_node = models.ManyToManyField(TemplateNode, related_name='template_node_responses')
    position_in_sequence = models.IntegerField()