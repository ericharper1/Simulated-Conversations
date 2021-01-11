from django.db import models
from embed_video.fields import EmbedVideoField
from django.urls import reverse
import uuid


class TemplateNode (models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    description = models.CharField(max_length=4000)
    video_url = EmbedVideoField(blank=False)
    start = models.BooleanField(default=False)
    terminal = models.BooleanField(default=False)
    parent_template = models.ForeignKey('conversation_templates.ConversationTemplate', default=0, related_name='template_nodes', on_delete=models.CASCADE)
    # For compatibility with forms. Field to hold pointers to destination template nodes (ManyToManyField)
    # To replace choice in tnc model. Field to hold list of text choices (ArrayField) Form: (SimpleArrayField)

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("conversation_step", kwargs={"ctn_id": self.id})
