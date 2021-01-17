from django import forms
from .models.template_node_choice import TemplateNodeChoice


class TemplateNodeChoiceForm(forms.Form):
    choices = forms.ModelChoiceField(
        queryset=None,
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        ct_node = kwargs.pop('ct_node', None)
        super(TemplateNodeChoiceForm, self).__init__(*args, **kwargs)
        self.fields['choices'].queryset = TemplateNodeChoice.objects.filter(parent_template=ct_node)
