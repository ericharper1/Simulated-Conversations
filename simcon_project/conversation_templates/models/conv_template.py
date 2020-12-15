from django.db import models
from django.utils import timezone


class ConversationTemplate (models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=4000)
    creation_date = models.DateTimeField(default=timezone.now)
    researcher = models.ForeignKey('users.Researcher', related_name='templates', on_delete=models.CASCADE)


