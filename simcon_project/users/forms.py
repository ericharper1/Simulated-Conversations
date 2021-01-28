from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from users.models import Student, SubjectLabel


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        #model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)


class NewStudentCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = Student
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2',)


class SendEmail(forms.Form):
    student_email = forms.EmailField(max_length=254, required=True)


class NewLabel(forms.Form):
    label_name = forms.CharField(max_length=100)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class UpdateFeedback(forms.Form):

    feedback = forms.CharField(help_text="Enter new Feedback")

