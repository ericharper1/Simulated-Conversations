from django.db import models
from .custom_user import CustomUser


class Student(CustomUser):
    researcher = models.ForeignKey('users.Researcher', related_name='researcher', on_delete=models.CASCADE)
# needs fixing
# ERRORS:
# users.Student.researcher: (models.E006) The field 'researcher' clashes with the field 'researcher' from model 'users.customuser'.
