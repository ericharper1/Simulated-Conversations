from django.db import models
import uuid


class TemplateNodeResponse (models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    transcription = models.CharField(max_length=1000)
    template_node = models.ForeignKey('conversation_templates.TemplateNode', default=0, related_name='responses', on_delete=models.DO_NOTHING)
    parent_template_response = models.ForeignKey('conversation_templates.TemplateResponse', default=0, related_name='node_responses', on_delete=models.CASCADE)
    selected_choice = models.ForeignKey('conversation_templates.TemplateNodeChoice', default=0, related_name='node_response', on_delete=models.DO_NOTHING)
    position_in_sequence = models.IntegerField()

    def __str__(self):
        return self.transcription
