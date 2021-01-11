from django.db import models
import uuid



class TemplateNodeChoice (models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    choice_text = models.CharField(max_length=500)
    destination_node = models.ForeignKey('conversation_templates.TemplateNode', default=0, related_name='parent_choices', on_delete=models.DO_NOTHING)
    parent_template = models.ForeignKey('conversation_templates.TemplateNode', default=0, related_name='choices', on_delete=models.DO_NOTHING)

    
