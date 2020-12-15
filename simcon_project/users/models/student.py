from django.db import models
from .custom_user import CustomUser


class Student(CustomUser):
    added_by = models.ForeignKey('users.Researcher', related_name='researcher', on_delete=models.CASCADE, default="None")
# needs fixing
# ERRORS:
# users.Student.researcher: (models.E006) The field 'researcher' clashes with the field 'researcher' from model 'users.customuser'.
