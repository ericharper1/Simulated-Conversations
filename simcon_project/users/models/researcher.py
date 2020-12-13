from django.db import models
from .custom_user import CustomUser
from conversation_templates.models.template import Template
from .assignment import Assignment
from .student import Student
from .subject_label import SubjectLabel

class Researcher(CustomUser):
    templates = models.ForeignKey(Template, on_delete=models.CASCADE)
    assignments = models.ForeginKey(Assignment, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='researchers')
    labels = models.ManyToManyField(SubjectLabel, related_name='researchers')