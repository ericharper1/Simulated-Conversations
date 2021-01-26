from django.db import models
import uuid


class TemplateNodeResponse (models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    transcription = models.CharField(max_length=1000)
    template_node = models.ForeignKey('conversation_templates.TemplateNode',default=0, related_name='responses', on_delete=models.DO_NOTHING)
    parent_template_response = models.ForeignKey('conversation_templates.TemplateResponse',default=0, related_name='node_responses', on_delete=models.CASCADE)
    position_in_sequence = models.IntegerField()
    feedback = models.CharField(max_length=1000, default=None)
    audio_response = models.FileField(upload_to='audio/%Y/%m/%d', default=None)

    def __str__(self):
        return f"{self.parent_template_response.student}: {self.template_node.description}, " \
               f"{self.parent_template_response.template.researcher} {self.position_in_sequence}"
