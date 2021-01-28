from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponseNotFound
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
    node_description = tables.Column()


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


def add_node_response(request, ct_node_id, ct_node_response_id):
    page_dict = request.session.get('page_dict')
    page_dict.update({str(ct_node_id): str(ct_node_response_id)})
    request.session.modified = True


def flush_session_data(request):
    if 'page_dict' in request.session:
        del request.session['page_dict']
    if 'ct_response_id' in request.session:
        del request.session['ct_response_id']
    if 'assign_id' in request.session:
        del request.session['assign_id']
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
                # Create the new response
                ct_node_response = TemplateNodeResponse.objects.create(
                    template_node=ct_node,
                    parent_template_response=ct_response,
                    selected_choice=choice,
                    position_in_sequence=ct_response.node_responses.count() + 1,
                    audio_response=None  # Don't have audio feature yet
                )
                # # Persist that node response id
                add_node_response(request, ct_node_id, ct_node_response.id)
            else:
                # For debugging, will be removed or changed before deploying to production
                return HttpResponseNotFound('An invalid choice was selected')

        # End conversation or go to next node
        if ct_node.terminal:
            return redirect(ct_response)
        return redirect(choice.destination_node)

    # GET request
    choice_form = TemplateNodeChoiceForm(ct_node=ct_node)
    ct = ct_node.parent_template
    # Check for page refresh
    if ct_node.start and request.session.get('ct_response_id') is None:
        ct_response = TemplateResponse.objects.create(
            student=Student.objects.get(email=request.user),
            template=ct,
            assignment=Assignment.objects.get(id=request.session.get('assign_id')),
        )
        request.session['ct_response_id'] = str(ct_response.id)  # persist the template response in the session
        request.session.modified = True

    ctx.update({
        'ct': ct,
        'ct_node': ct_node,
        'choice_form': choice_form,
    })
    return render(request, t, ctx)


@user_passes_test(is_student)
def conversation_end(request, ct_response_id):
    ctx = {}
    t = '{}/conversation_end.html'.format(ct_templates_dir)
    ct_response = TemplateResponse.objects.get(id=ct_response_id)
    ct = ct_response.template

    ct_node_responses = TemplateNodeResponse.objects.filter(parent_template_response=ct_response) \
        .order_by('position_in_sequence')

    # Create a dict to send to table creation method
    table_contents = []
    for response in ct_node_responses:
        table_contents.append({'node_description': response.template_node.description})
    ct_node_table = NodeDescriptionTable(table_contents)

    # POST request
    if request.method == 'POST':
        for response in ct_node_responses:
            response.transcription = request.POST.get(str(response.id), '')
            response.save()
        if ct_response.completion_date is None:
            ct_response.completion_date = timezone.now()
            ct_response.save()
        return redirect('StudentView')

    # GET request
    ctx.update({
        'ct': ct,
        'ct_response': ct_response,
        'ct_node_table': ct_node_table,
        'ct_node_responses': ct_node_responses
    })
    return render(request, t, ctx)
