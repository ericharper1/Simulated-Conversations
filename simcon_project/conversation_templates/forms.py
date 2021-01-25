from django import forms
from .models import TemplateFolder, TemplateNodeChoice
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
        self.fields['name'].required = True

    class Meta:
        model = TemplateFolder
        fields = ['name', 'templates']
        widgets = {'templates': SelectTemplates}


class TemplateNodeChoiceForm(forms.Form):
    """
    Form to display choices related to a TemplateNode
    """
    choices = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        ct_node = kwargs.pop('ct_node', None)
        super(TemplateNodeChoiceForm, self).__init__(*args, **kwargs)
        self.fields['choices'].queryset = TemplateNodeChoice.objects.filter(parent_template=ct_node)
