from django import forms
from .models import TemplateFolder, ConversationTemplate


class SelectTemplates(forms.SelectMultiple):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        return option


class FolderCreationForm(forms.ModelForm):
    class Meta:
        model = TemplateFolder
        fields = ['name', 'templates']
        widgets = {'templates': SelectTemplates}
