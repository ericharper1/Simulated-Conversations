import os

from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from conversation_templates.models import ConversationTemplate, TemplateNode, TemplateNodeResponse, TemplateResponse
from conversation_templates.forms import TemplateNodeChoiceForm
from users.models import Student, Assignment
from django.contrib.auth.decorators import user_passes_test
from users.views.student_home import is_student
import django_tables2 as tables

# Globals
ct_templates_dir = 'conversation'


class NodeDescriptionTable(tables.Table):
    """
    Creates table that displays the description for each TemplateNode object that a Student visited.
    """
    position = tables.Column(accessor='position_in_sequence')
    description = tables.Column(accessor='template_node__description')


def if_visited(request, ct_node_id):
    page_dict = request.session.get('page_dict')
    if not page_dict:
        return False
    if page_dict.get(str(ct_node_id)):
        return True
    return False


def get_node_response(request, ct_node_id):
    page_dict = request.session.get('page_dict')
    return TemplateNodeResponse.objects.get(id=page_dict.get(str(ct_node_id)))


# Tracks pages that have been completed
def mark_page_complete(request, ct_node_id, ct_node_response_id):
    page_dict = request.session.get('page_dict')
    page_dict.update({str(ct_node_id): str(ct_node_response_id)})
    request.session.modified = True


# Clear things from past user session
def flush_session_data(request):
    if 'page_dict' in request.session:
        del request.session['page_dict']
    if 'ct_response_id' in request.session:
        del request.session['ct_response_id']
    if 'assign_id' in request.session:
        del request.session['assign_id']
    if 'ct_node_response_id' in request.session:
        del request.session['ct_node_response_id']
    request.session.modified = True


# Views
@user_passes_test(is_student)
def conversation_start(request, ct_id, assign_id):
    """
    Renders entry page for a conversation. Student can choose to start the conversation or go back.
    """
    ctx = {}
    t = '{}/conversation_start.html'.format(ct_templates_dir)
    ct = ConversationTemplate.objects.get(id=ct_id)
    ct_node = TemplateNode.objects.get(parent_template=ct, start=True)

    # Clear existing session data leftover from incomplete response
    flush_session_data(request)
    request.session['assign_id'] = assign_id
    request.session['page_dict'] = {}
    ctx.update({
        'ct': ct,
        'ct_node': ct_node,
    })
    return render(request, t, ctx)


@user_passes_test(is_student)
def conversation_step(request, ct_node_id):
    """
    Renders each step in a conversation where a Student can watch the video, record a response,
    and select a choice.
    """
    ctx = {}
    t = '{}/conversation_step.html'.format(ct_templates_dir)
    ct_node = TemplateNode.objects.get(id=ct_node_id)
    ct_node_response_id = request.session.get('ct_node_response_id')
    audio_response = None

    # POST request
    if request.method == 'POST':
        choice = None
        ct_response_id = request.session.get('ct_response_id')
        if ct_response_id is None:
            # For debugging, will remove once in production
            return HttpResponseNotFound('Conversation Template Response does not exist for current session.')
        ct_response = TemplateResponse.objects.get(id=ct_response_id)

        # check if node response has already been made - User attempting to resubmit POST
        if if_visited(request, ct_node_id):
            node_response = get_node_response(request, ct_node_id)
            choice = node_response.selected_choice
        else:
            choice_form = TemplateNodeChoiceForm(request.POST, ct_node=ct_node)
            if choice_form.is_valid():
                choice = choice_form.cleaned_data['choices']

                # Edit node response to add remaining fields
                update_node_response = TemplateNodeResponse.objects.get(id=request.session.get('ct_node_response_id'))
                update_node_response.template_node = ct_node
                update_node_response.selected_choice = choice
                update_node_response.save()

                # Persist that node response id
                mark_page_complete(request, ct_node_id, ct_node_response_id)
                del request.session['ct_node_response_id']
                request.session.modified = True
            else:
                # For debugging, will be removed or changed before deploying to production
                return HttpResponseNotFound('An invalid choice was selected')

        # End conversation or go to next node
        if ct_node.terminal:
            return redirect(ct_response)
        return redirect(choice.destination_node)

    # GET request
    choice_form = TemplateNodeChoiceForm(ct_node=ct_node)
    ct = ct_node.parent_template_node

    # Check for page refresh
    if ct_node.start and request.session.get('ct_response_id') is None:
        ct_response = TemplateResponse.objects.create(
            student=Student.objects.get(email=request.user),
            template=ct,
            assignment=Assignment.objects.get(id=request.session.get('assign_id')),
        )
        request.session['ct_response_id'] = str(ct_response.id)  # persist the template response in the session
        request.session.modified = True
    # Check if audio already exists
    if ct_node_response_id:
        ct_node_response = TemplateNodeResponse.objects.get(id=ct_node_response_id)
        audio_response = ct_node_response.audio_response

    ctx.update({
        'ct': ct,
        'ct_node': ct_node,
        'choice_form': choice_form,
        'audio_response': audio_response,
    })
    return render(request, t, ctx)


@csrf_exempt
def save_audio(request):
    # Check if node response already exists
    if request.session.get('ct_node_response_id') is None:
        # Get audio blob from session
        data = request.FILES.get('data')
        file_handle = str(timezone.now())
        file_handle = file_handle.replace(':', '-') + '.wav'
        file_handle = os.path.join('audio', str(request.user), file_handle)  # Create full file handle
        audio_path = default_storage.save(file_handle, data)  # Store audio in media root
        ct_response = TemplateResponse.objects.get(id=request.session.get('ct_response_id'))
        ct_node_response = TemplateNodeResponse.objects.create(
            template_node=None,
            parent_template_response=ct_response,
            selected_choice=None,
            position_in_sequence=ct_response.node_responses.count() + 1,
            audio_response=audio_path
        )
        request.session['ct_node_response_id'] = ct_node_response.id
        return HttpResponse('saved')
    else:
        return HttpResponse('audio response already exists')


@user_passes_test(is_student)
def conversation_end(request, ct_response_id):
    ctx = {}
    t = '{}/conversation_end.html'.format(ct_templates_dir)
    ct_response = TemplateResponse.objects.get(id=ct_response_id)
    ct = ct_response.template

    # Get responses in order
    ct_node_responses = TemplateNodeResponse.objects.filter(parent_template_response=ct_response) \
        .order_by('position_in_sequence')
    response_table_content = ct_node_responses.values(
        'position_in_sequence',
        'template_node__description',
        'audio_response'
    )
    ct_node_table = NodeDescriptionTable(response_table_content)

    # POST request
    if request.method == 'POST':
        for response in ct_node_responses:
            response.transcription = request.POST.get(str(response.id), '')
            response.save()
        if ct_response.completion_date is None:
            ct_response.completion_date = timezone.now()
            ct_response.save()
        return redirect('student-view')

    # GET request
    ctx.update({
        'ct': ct,
        'ct_response': ct_response,
        'ct_node_table': ct_node_table,
        'ct_node_responses': ct_node_responses
    })
    return render(request, t, ctx)
