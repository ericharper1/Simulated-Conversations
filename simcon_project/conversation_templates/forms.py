from django import forms
from .models import TemplateFolder
from bootstrap_modal_forms.forms import BSModalModelForm


class FolderCreationForm(forms.Form):
    name = forms.CharField(label="", max_length=50,  widget=forms.TextInput(attrs={'placeholder': 'Enter Folder Name'}))


class FolderModalForm(BSModalModelForm):
    class Meta:
        model = TemplateFolder
        fields = ['name']
