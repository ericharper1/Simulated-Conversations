from django.db import models
import uuid


class TemplateNodeChoice(models.Model):
    """
    Contains information for a choice that a Student can choose on a TemplateNode object
    Fields:
    id: Primary key id for TemplateNodeChoice object
    choice_text: A text description for the Choice object
    destination_node: The TemplateNode object that a Choice object leads to
    parent_template: The TemplateNode object that a Choice object belongs to
    """
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    choice_text = models.CharField(max_length=500)
    destination_node = models.ForeignKey('conversation_templates.TemplateNode', default=0, null=True, blank=True, related_name='parent_choices', on_delete=models.DO_NOTHING)
    parent_template = models.ForeignKey('conversation_templates.TemplateNode', default=0, related_name='choices', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.choice_text
