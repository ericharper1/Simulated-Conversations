from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from users.models import Student, SubjectLabel
import django_tables2 as tables



class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)


class NewStudentCreationForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    password1 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)


class StudentTable(tables.Table):
    class Meta:
        model = Student


class LabelTable(tables.Table):
    class Meta:
        model = SubjectLabel


class SendEmail(forms.Form):
    new = forms.BooleanField(required=False)
    student_email = forms.EmailField(max_length=254, required=True)


class NewLabel(forms.Form):
    label_name = forms.CharField(max_length=100)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class UpdateFeedback(forms.Form):

    feedback = forms.CharField(help_text="Enter new Feedback")

