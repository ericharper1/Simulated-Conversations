from django.db import models
from conversation_templates.models.conv_template import ConversationTemplate
from .custom_user import CustomUser
from .assignment import Assignment
from .student import Student
from .subject_label import SubjectLabel


class Researcher(CustomUser):
    templates = models.ForeignKey(ConversationTemplate, on_delete=models.CASCADE)
    assignments = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='researchers')
    labels = models.ManyToManyField(SubjectLabel, related_name='researchers')