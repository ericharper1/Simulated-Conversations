from django.shortcuts import render, redirect
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model
from conversation_templates.models.conv_template import ConversationTemplate
from conversation_templates.models.template_node import TemplateNode
from conversation_templates.models.template_node_choice import TemplateNodeChoice
# from conversation_templates.forms import TemplateNodeResponseCreateForm
# from conversation_templates.forms import TemplateNodeChoiceForm

# Globals
ct_templates_dir = 'conversation'
user = get_user_model()


# Views
def conversation_start(request, ct_id):
    ctx = {}
    ct = ConversationTemplate.objects.get(id=ct_id)
    ctn = TemplateNode.objects.get(parent_template=ct, start=True)
    ctx.update({'ct': ct})
    ctx.update({'ctn': ctn})
    t = '{}/conversation_start.html'.format(ct_templates_dir)
    return render(request, t, ctx)


def conversation_step(request, ctn_id):  # a08b1b1a-e3fe-4c5b-9639-66a4f895c103
    ctx = {}
    ctn = TemplateNode.objects.get(id=ctn_id)  # get conversation template node from choice
    formset = None
    if request.method == 'POST':
        # choice_form = TemplateNodeChoiceForm(data=request.POST)
        # if choice_form.is_valid():
        print('selected choice: ' + str(request.POST))
        print('Yes')
            # print(choice_form.cleaned_data())
        # else:
        #     print('No')
            # print(choice_form.errors['choices'])
    else:
        ctn = TemplateNode.objects.get(id=ctn_id)  # get conversation template node from url
        choice_form_set = inlineformset_factory(
            TemplateNode,
            TemplateNodeChoice,
            fk_name='parent_template',
            fields=('choice_text',),
        )
        formset = choice_form_set(instance=ctn)

    ct = ctn.parent_template
    end = False
    if ctn.start:  # logic for beginning or ending a conversation
        pass
    elif ctn.terminal:
        end = True
    ctx.update({
        "ct": ct,
        "ctn": ctn,
        "choice_form": formset,
        "end": end,
    })
    t = '{}/conversation_step.html'.format(ct_templates_dir)
    return render(request, t, ctx)

# def conversation_step(request, ctn_id):  # a08b1b1a-e3fe-4c5b-9639-66a4f895c103
#     ctx = {}
#     ctn = TemplateNode.objects.get(id=ctn_id)  # get conversation template node from choice
#     cntc = TemplateNodeChoice.objects.get(id='ffe72335-9e17-41f1-bef5-357a191ed75a')
#     print(cntc)
#     print(type(request.POST.get('choices')))
#
#     if request.method == 'POST':
#         choice_form = TemplateNodeChoiceForm(data=request.POST)
#         if choice_form.is_valid():
#             print('Yes')
#             print(choice_form.cleaned_data())
#         # process data in form cleaned
#             # dest_ctn_id = choice_form.cleaned_data()
#             # ctn = TemplateNode.objects.get(id=dest_ctn_id)  # get conversation template node from choice
#         else:
#             print('No')
#             print(choice_form.errors['choices'])
#     else:
#         ctn = TemplateNode.objects.get(id=ctn_id)  # get conversation template node from url
#         ctn_choices = TemplateNodeChoice.objects.filter(parent_template=ctn)
#         choices = []
#         for choice in ctn_choices:
#             choices.append((str(choice.id), choice.choice_text))
#         print(choices)
#         choice_form = TemplateNodeChoiceForm()
#         choice_form.fields["choices"].choices = choices
#         print(choice_form)
#
#     ct = ctn.parent_template
#     end = False
#     if ctn.start:  # logic for beginning or ending a conversation
#         pass
#     elif ctn.terminal:
#         end = True
#     ctx.update({
#         "ct": ct,
#         "ctn": ctn,
#         "choice_form": choice_form,
#         "end": end,
#     })
#     t = '{}/conversation_step.html'.format(ct_templates_dir)
#     return render(request, t, ctx)


def conversation_end(request):
    ctx = {}
    # for testing
    ct_list = [
        {
            'description': 'scene1',
            'transcription': 'response1'
        },
        {
            'description': 'scene2',
            'transcription': 'response2'
        },
        {
            'description': 'scene3',
            'transcription': 'response3'
        }
    ]

    ctx.update({'ct_list': ct_list})
    t = '{}/conversation_end.html'.format(ct_templates_dir)
    return render(request, t, ctx)
