from django import forms
from .models import TemplateFolder, ConversationTemplate
from django.core.exceptions import ValidationError
from bootstrap_modal_forms.forms import BSModalModelForm


class SelectTemplates(forms.SelectMultiple):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        return option


class FolderCreationForm(BSModalModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True

    class Meta:
        model = TemplateFolder
        fields = ['name', 'templates']
        widgets = {'templates': SelectTemplates}

    #def clean(self):
    #    super(FolderCreationForm, self).clean()
    #    name = self.cleaned_data.get('name')
    #    templates = self.cleaned_data.get('templates')
    #    max_len = TemplateFolder._meta.get_field('name').max_length
    #    if len(name) < max_len:
    #        self.add_error('name', "hello")

    #    return self.cleaned_data
