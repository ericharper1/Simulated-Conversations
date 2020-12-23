from django.db import models
import uuid


class FolderManager (models.Manager):

    def create_folder(self, name):
        folder = self.create(name=name)
        return folder


class TemplateFolder (models.Model):
    """
    A Folder containing (only) templates

    Fields:
    id: UUID to uniquely identify a folder. Primary Key
    name: Name of the folder
    templates: Templates associated to the folder.
        Templates can be associated to more than one file.

    """
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    templates = models.ManyToManyField('conversation_templates.ConversationTemplate', related_name='folder', blank=True)
    objects = FolderManager()
