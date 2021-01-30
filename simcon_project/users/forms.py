from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import ModelForm
from .models import CustomUser, Researcher


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class UpdateFeedback(forms.Form):

    feedback = forms.CharField(help_text="Enter new Feedback")


class NewResearcherCreationForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    password1 = forms.CharField(max_length=100, required=True)
    password2 = forms.CharField(max_length=100, required=True)


class AddResearcherForm(ModelForm):

    class Meta:
        model = Researcher
        fields = ['email']
