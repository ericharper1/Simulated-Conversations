from django.db import models
#from .template_node import TemplateNode


class TemplateNodeChoice (models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True)
    choice_text = models.CharField(max_length=500)
    #node_id = models.OneToOneField(TemplateNode, related_name='template_node_choice')