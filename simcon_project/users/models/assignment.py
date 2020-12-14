from django.db import models
from conversation_templates.models.template import Template
from .student import Student
from .subject_label import SubjectLabel

class Assignment(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=100) 
    date_assigned = models.DateField()
    templates = models.ForeignKey(Template, related_name='assignments')
    students = models.ManyToMany(Student, related_name='assignments')
    labels = models.ManyToMany(SubjectLabel, related_name='assignments')

    def get_name(self):
        return self.name

    def get_date_assigned(self):
        return self.date_assigned