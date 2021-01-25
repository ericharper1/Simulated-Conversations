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


class DeleteResearchersForm(ModelForm):

    class Meta:
        model = Researcher
        fields = ('email',)


class AddResearcherForm(ModelForm):

    class Meta:
        model = Researcher
        fields = ['first_name', 'last_name', 'email']
