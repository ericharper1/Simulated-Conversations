from django import forms
from django.core.exceptions import ValidationError
from .models.template_node_response import TemplateNodeResponse
from .models.template_node import TemplateNode
from .models.template_node_choice import TemplateNodeChoice





# class TemplateNodeResponseCreateForm(forms.ModelForm):
#     class Meta:
#         model = TemplateNodeResponse
#         fields = [
#             'transcription',
#         ]


# class TemplateNodeChoiceForm(forms.Form):
#     def validate_choice(self):
#         choices = self.cleaned_data['choices']
#         if not TemplateNodeChoice.objects.get(id=choices):
#             raise ValidationError(f'Destination node with ID {choices} does not exist.')
#         return choices
#
#     # def form_valid(self):
#
#
#     choices = forms.ChoiceField(
#         choices=(),
#         widget=forms.RadioSelect,
#         validators=[validate_choice],
#     )


# class TemplateNodeChoiceForm(forms.Form):
#     choices = forms.ModelChoiceField(
#         queryset=TemplateNodeChoice.objects.none(),
#         widget=forms.RadioSelect,
#     )

# Doesn't work because it doesn't recognize field 'choices'
# class TemplateNodeChoiceForm(forms.ModelForm):
#     class Meta:
#         model = TemplateNode
#         fields = [
#             'choices',
#         ]
#
#     choices = forms.ModelChoiceField(queryset=self.instance.objects.all())

# class TemplateNodeChoiceForm(forms.Form):
#     choices = forms.ModelChoiceField(
#         queryset=None,
#         widget=forms.RadioSelect,
#     )
#
#     def __init__(self, *args, **kwargs):
#         ctn = kwargs.pop('ctn', None)
#         super(TemplateNodeChoiceForm, self).__init__(*args, **kwargs)
#         # self.fields['choices'].queryset = TemplateNodeChoice.objects.filter(parent_template=ctn)
#         self.fields['choices'].queryset = self.instance.choices.all()
