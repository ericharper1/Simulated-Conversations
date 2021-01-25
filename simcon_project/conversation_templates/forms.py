from django import forms
from .models import TemplateFolder
from .models import ConversationTemplate
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from bootstrap_modal_forms.forms import BSModalModelForm


class SelectTemplates(forms.SelectMultiple):
    """
    Function needed to make the multiple templates selectable within the form.
    """
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)
        return option


class FolderCreationForm(BSModalModelForm):
    """
    Form to create a TemplateFolder object
    Uses BSModalModelForm which is needed for bootstrap_modal_forms to work properly
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show templates unique to each user in the form.
        if self.request.user:
            templates = ConversationTemplate.objects.filter(researcher=self.request.user.id)
            self.fields['templates'].queryset = templates.all()
        self.fields['name'].required = True

    class Meta:
        model = TemplateFolder
        fields = ['name', 'templates']
        widgets = {'templates': SelectTemplates}
