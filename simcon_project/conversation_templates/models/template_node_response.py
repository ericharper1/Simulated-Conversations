from django.db import models


class TemplateNodeResponse (models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True)
    transcription = models.CharField(max_length=1000)
    template_node = models.ForeignKey('conversation_templates.TemplateNode',default=0, related_name='responses', on_delete=models.DO_NOTHING)
    position_in_sequence = models.IntegerField()
