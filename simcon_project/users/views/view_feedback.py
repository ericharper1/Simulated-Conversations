from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from conversation_templates.models import TemplateResponse, TemplateNodeResponse


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def ViewFeedback(request, pk=None):
    response = get_object_or_404(TemplateResponse, pk=pk)

    nodes = []
    num_nodes = TemplateNodeResponse.objects.filter(parent_template_response=response).count()
    for i in range(1, num_nodes+1):
        if TemplateNodeResponse.objects.get(parent_template_response=response, position_in_sequence=i):
            nodes.append(TemplateNodeResponse.objects.get(parent_template_response=response,
                                                          position_in_sequence=i))
        else:
            break
    return render(request, 'view_feedback.html', {'response_nodes': nodes, 'response': response})
