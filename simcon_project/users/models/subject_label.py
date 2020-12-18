from django.db import models
import uuid


class SubjectLabel(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    label_name = models.CharField(max_length=100)
    students = models.ManyToManyField('users.Student', related_name='labels')
    researcher = models.ForeignKey('users.Researcher', related_name='labels', default=0, on_delete=models.CASCADE)

    def get_file_name(self):
        return self.file_name
