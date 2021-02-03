from django import forms
from django.db.models.functions import Lower
from .models import TemplateFolder, TemplateNodeChoice, ConversationTemplate
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


class NodeChoiceWidget(forms.RadioSelect):
    def __init__(self, name, data_list, *args, **kwargs):
        super(NodeChoiceWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._list = data_list

    def render(self, name, value, attrs=None, renderer=None):
        choice_html = f'<ul id="id_{name}">'
        for idx, choice in enumerate(self._list):

            choice_html += f'<li><label for="id_choice-{idx}"><input type="radio" id="id_choice-{idx}"' \
                            f'name={name} value="{choice.id}"> {choice.choice_text}  </label></li>'

        choice_html += f'<li><label for="id_choice-custom"><input type="radio" id="id_choice-custom"' \
                       f'name={name} value="custom-response"><input name="custom-text" type="text" ' \
                       f'placeholder="Enter Custom Response" id="id_custom-input"></label></li>'

        choice_html += '</ul>'

        return choice_html


class TemplateNodeChoiceForm(forms.Form):
    """
    Form to display choices related to a TemplateNode
    """
    choices = forms.ModelChoiceField(
        queryset=None,
    )

    def __init__(self, *args, **kwargs):
        ct_node = kwargs.pop('ct_node', None)
        choice_list = TemplateNodeChoice.objects.filter(parent_template=ct_node)
        super(TemplateNodeChoiceForm, self).__init__(*args, **kwargs)
        self.fields['choices'].queryset = TemplateNodeChoice.objects.filter(parent_template=ct_node)
        self.fields['choices'].widget = NodeChoiceWidget(name="hello", data_list=choice_list)

    def is_valid(self):
        valid = super(TemplateNodeChoiceForm, self).is_valid()

        if not valid and self.data['choices'] != 'custom-response':
            return False

        return True
