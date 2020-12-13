from django.db import models
from conversation_templates.models.template import Template
from .student import Student
from .subject_label import SubjectLabel

class Assignment():
    id = models.UUIDField(unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=100) 
    creation_date = models.DateField()
    templates = models.ForeignKey(Template, related_name='assignments')
    students = models.ManyToMany(Student, related_name='assignments')
    labels = models.ManyToMany(SubjectLabel, related_name='assignments')

    def get_name(self):
        return self.name

    def get_creation_date(self):
        return self.creation_date