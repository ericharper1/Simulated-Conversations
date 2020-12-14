from django.db import models


class SubjectLabel(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True)
    file_name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, related_name='subject_labels')

    def get_file_name(self):
        return self.file_name