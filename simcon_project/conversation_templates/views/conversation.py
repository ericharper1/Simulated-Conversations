from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.forms import modelformset_factory
from conversation_templates.models.conv_template import ConversationTemplate
from conversation_templates.models.template_node import TemplateNode
from conversation_templates.models.template_node_response import TemplateNodeResponse
from conversation_templates.models.template_response import TemplateResponse
from conversation_templates.forms import TemplateNodeChoiceForm
from users.models.student import Student
from users.models.assignment import Assignment
from datetime import datetime
from django.contrib.auth.decorators import login_required
import django_tables2 as tables

# Globals
ct_templates_dir = 'conversation'


class NodeDescriptionTable(tables.Table):
    """
    Creates table that displays the description for each TemplateNode object that a Student visited.
    """
    node_description = tables.Column()


# Views
@login_required(login_url='/accounts/login/')
def conversation_start(request, ct_id, assign_id):
    """
    Renders entry page for a conversation. Student can choose to start the conversation or go back.
    """
    ctx = {}
    ct = ConversationTemplate.objects.get(id=ct_id)
    ct_node = TemplateNode.objects.get(parent_template=ct, start=True)
    request.session['assign_id'] = assign_id
    ctx.update({'ct': ct})
    ctx.update({'ct_node': ct_node})
    t = '{}/conversation_start.html'.format(ct_templates_dir)
    return render(request, t, ctx)


@login_required(login_url='/accounts/login/')
def conversation_step(request, ct_node_id):
    """
    Renders each step in a conversation where a Student can watch the video, record a response,
    and select a choice.
    """
    ctx = {}
    ct_node = TemplateNode.objects.get(id=ct_node_id)

    # POST request
    if request.method == 'POST':
        choice_form = TemplateNodeChoiceForm(request.POST, ct_node=ct_node)
        if choice_form.is_valid():
            choice = choice_form.cleaned_data['choices']
            ct_response_id = request.session.get('ct_response_id')
            if ct_response_id is None:
                # For debugging, will remove once in production
                return HttpResponseNotFound('Conversation Template Response does not exist for current session.')
            ct_response = TemplateResponse.objects.get(id=ct_response_id)
            TemplateNodeResponse.objects.create(
                transcription='',
                template_node=ct_node,
                parent_template_response=ct_response,
                selected_choice=choice,
                position_in_sequence=ct_response.node_responses.count() + 1,
                audio_response=None  # Don't have audio feature yet
            )
            # Grab next node or direct to conversation end
            response_object = choice.destination_node
            if not response_object:
                response_object = ct_response
            return redirect(response_object)
        else:
            # For debugging, will be removed or changed before deploying to production
            return HttpResponseNotFound('An invalid choice was selected')

    # GET request
    ct_node = TemplateNode.objects.get(id=ct_node_id)
    choice_form = TemplateNodeChoiceForm(ct_node=ct_node)
    ct = ct_node.parent_template
    if ct_node.start and request.session.get('ct_response_id') is None:
        ct_response = TemplateResponse.objects.create(
            student=Student.objects.get(email=request.user),
            template=ct,
            assignment=Assignment.objects.get(id=request.session.get('assign_id')),
        )
        request.session['ct_response_id'] = str(ct_response.id)  # persist the template response in the session
    ctx.update({
        'ct': ct,
        'ct_node': ct_node,
        'choice_form': choice_form,
    })
    t = '{}/conversation_step.html'.format(ct_templates_dir)
    return render(request, t, ctx)


@login_required(login_url='/accounts/login/')
def conversation_end(request, ct_response_id):
    ctx = {}
    ct_response = TemplateResponse.objects.get(id=ct_response_id)
    ct = ct_response.template
    trans_formset = modelformset_factory(TemplateNodeResponse, fields=('transcription',), extra=0)
    t = '{}/conversation_end.html'.format(ct_templates_dir)
    ct_node_responses = TemplateNodeResponse.objects.filter(parent_template_response=ct_response) \
        .order_by('position_in_sequence')
    formset = trans_formset(queryset=ct_node_responses)
    table_contents = []
    for response in ct_node_responses:
        table_contents.append({'node_description': response.template_node.description})
    ct_node_table = NodeDescriptionTable(table_contents)
    ctx.update({
        'ct': ct,
        'formset': formset,
        'ct_response': ct_response,
        'ct_node_table': ct_node_table,
    })

    # POST request
    if request.method == 'POST':
        formset = trans_formset(request.POST)
        if formset.is_valid():
            formset.save()
            if ct_response.completion_date is None:
                ct_response.completion_date = datetime.now()
                ct_response.save()
            return redirect('StudentView')
        else:
            # return page with errors
            print('formset not valid.')
            print(formset.errors)
            ctx.update({'formset_error': '*Transcription fields are required.'})
            return render(request, t, ctx)

    # GET request
    if 'ct_response_id' in request.session:
        del request.session['ct_response_id']
        request.session.modified = True
    if 'assign_id' in request.session:
        del request.session['assign_id']
        request.session.modified = True
    return render(request, t, ctx)
