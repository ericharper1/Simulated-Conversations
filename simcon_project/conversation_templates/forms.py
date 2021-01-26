from django import forms
from django.db.models.functions import Lower
from .models import TemplateFolder
from .models import ConversationTemplate
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


class SelectTemplateForm(forms.Form):
    """
    Form containing a single ChoiceField to select a template.
    The template being viewed right now will be the initial value in the ChoiceField and others
    are ordered in alphabetical order (case insensitive).
    Each choice is a tuple of (template.id, template.name) so template id can be used when the
    form is submitted on a POST request.
    """

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        initial = kwargs.pop('initial')
        super().__init__(*args, **kwargs)
        if request.user and initial:
            templates = ConversationTemplate.objects.filter(researcher=request.user.id).exclude(name=initial).order_by(Lower('name'))
            template_list = [(ConversationTemplate.objects.get(name=initial).id, initial)]
            for template in templates:
                template_list.append((template.id, template.name))
            self.fields['templates'] = forms.ChoiceField(choices=template_list)
