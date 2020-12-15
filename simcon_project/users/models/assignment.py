from django.db import models
from conversation_templates.models.conv_template import ConversationTemplate
from .student import Student
from .subject_label import SubjectLabel


class Assignment(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=100) 
    date_assigned = models.DateField()
    templates = models.ForeignKey(ConversationTemplate, related_name='assignments', on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='assignments')
    labels = models.ManyToManyField(SubjectLabel, related_name='assignments')

    def get_name(self):
        return self.name

    def get_date_assigned(self):
        return self.date_assigned