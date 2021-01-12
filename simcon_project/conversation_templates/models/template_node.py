from django.db import models
from embed_video.fields import EmbedVideoField
import uuid


class TemplateNode (models.Model):
    """
    Stores description and video for a node in a conversation, and has
    fields to signify if node is the first or the last in a conversation.
    Related to :model:`conversation_templates.ConversationTemplate`.
    """
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    description = models.CharField(max_length=4000)
    video_url = EmbedVideoField(blank=False)
    start = models.BooleanField(default=False)
    terminal = models.BooleanField(default=False)
    parent_template = models.ForeignKey('conversation_templates.ConversationTemplate', default=0, related_name='template_nodes', on_delete=models.CASCADE)
