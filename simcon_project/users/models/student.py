from django.db import models
from .custom_user import CustomUser


class Student(CustomUser):
    added_by = models.ForeignKey('users.Researcher', default=0, related_name='students', on_delete=models.CASCADE)