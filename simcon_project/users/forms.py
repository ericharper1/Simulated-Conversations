from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models.custom_user import CustomUser, CustomUserManager
from users.models import Student

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        #model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)


class NewStudentCreationForm(CustomUserManager):

    class Meta(CustomUserManager):
        model = Student
        model.email = 'email'#wrong not CustomUserManager need to find self ref
        model.password = 'password'

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = Student
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2', )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)