from django.db import models


class TemplateNodeChoice (models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True)
    choice_text = models.CharField(max_length=500)
    destination_node = models.ForeignKey('conversation_templates.TemplateNode', default=0, related_name='destination_choices', on_delete=models.DO_NOTHING)
    parent_template = models.ForeignKey('conversation_templates.TemplateNode', default=0, related_name='choices', on_delete=models.DO_NOTHING)
