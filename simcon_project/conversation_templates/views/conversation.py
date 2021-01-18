from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponse
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

# Globals
ct_templates_dir = 'conversation'


# Views
@login_required
def conversation_start(request, ct_id):
    ctx = {}
    ct = ConversationTemplate.objects.get(id=ct_id)  # Get current Conversation Template
    ct_node = TemplateNode.objects.get(parent_template=ct, start=True)  # Get first node
    print(request.session.get('ct_response_id'))  # Should be None at this point
    # Create context object
    ctx.update({'ct': ct})
    ctx.update({'ct_node': ct_node})
    t = '{}/conversation_start.html'.format(ct_templates_dir)
    return render(request, t, ctx)


@login_required()
def conversation_step(request, ct_node_id):  # Conversation Template(testing): b59cfc4c-b6ab-488b-bcef-3c69d137c64b
    ctx = {}
    ct_node = TemplateNode.objects.get(id=ct_node_id)  # get conversation template node from url
    # POST request
    if request.method == 'POST':
        choice_form = TemplateNodeChoiceForm(request.POST, ct_node=ct_node)
        if choice_form.is_valid():
            choice = choice_form.cleaned_data['choices']
            ct_response_id = request.session.get('ct_response_id')
            if not ct_response_id:
                return HttpResponse('<h1>Conversation Template Response does not exist for current session.</h1>')
            ct_response = TemplateResponse.objects.get(id=ct_response_id)  # grab template response
            # Create node response for current node
            ct_node_response = TemplateNodeResponse.objects.create(
                transcription='',
                template_node=ct_node,
                parent_template_response=ct_response,
                selected_choice=choice,
                position_in_sequence=ct_response.node_responses.count() + 1,
                feedback='',  # won't have feedback until after convo is finished
                audio_response=None
            )
            # Grab next node or direct to conversation end
            response_object = choice.destination_node
            if not response_object:
                response_object = ct_response
            return redirect(response_object)
        else:
            # Need better 404 message
            # this should also never trigger
            return HttpResponseNotFound('Form was not valid')

    # GET request
    ct_node = TemplateNode.objects.get(id=ct_node_id)  # get conversation template node from url
    choice_form = TemplateNodeChoiceForm(ct_node=ct_node)  # populate form with choices
    ct = ct_node.parent_template
    if ct_node.start and request.session.get('ct_response_id') is None:  # also check if we already made a response - user could have refreshed the page.
        ct_response = TemplateResponse.objects.create(
            student=Student.objects.get(email=request.user),  # Grab static student - testing
            template=ct,
            assignment=Assignment.objects.get(id='6f3090fa-84a4-408d-99f9-5bbd5fccfbb3'),  # Grab static assignment - testing
            feedback=''
        )
        request.session['ct_response_id'] = str(ct_response.id)  # persist the template response
    print(request.session.get('ct_response_id'))
    ctx.update({
        'ct': ct,
        'ct_node': ct_node,
        'choice_form': choice_form,
    })
    t = '{}/conversation_step.html'.format(ct_templates_dir)
    return render(request, t, ctx)


@login_required()
def conversation_end(request, ct_response_id):
    ctx = {}
    ct_response = TemplateResponse.objects.get(id=ct_response_id)
    trans_formset = modelformset_factory(TemplateNodeResponse, fields=('transcription',), extra=0)

    # POST request
    if request.method == 'POST':
        print('caught post request')
        trans_form = trans_formset(request.POST)
        if trans_form.is_valid():
            trans_form.save()

    # GET request
    if 'ct_response_id' in request.session:
        del request.session['ct_response_id']  # Don't need template response anymore
        request.session.modified = True  # Saves session update
    # should conversation be considered finished after last node, or upon finishing transcriptions on final page?
    # Set completion date if not already set - user might refresh the page
    if ct_response.completion_date is None:
        ct_response.completion_date = datetime.now()
        ct_response.save()
    ct = ct_response.template
    student = ct_response.student
    # ct_node_responses = ct_response.node_responses  # not working?
    ct_node_responses = TemplateNodeResponse.objects.filter(parent_template_response=ct_response)
    print(ct_node_responses)
    trans_form = trans_formset(
        queryset=TemplateNodeResponse.objects.filter(parent_template_response=ct_response)
        .order_by('position_in_sequence')
    )
    ctx.update({
        'ct': ct,
        'student': student,
        'trans_form': trans_form,
        'ct_response': ct_response,
        'ct_node_responses': ct_node_responses,
    })
    t = '{}/conversation_end.html'.format(ct_templates_dir)
    return render(request, t, ctx)
