from django.shortcuts import render
from conversation_templates.models import TemplateResponse, TemplateNodeResponse


def ViewResponse(request, responseid="6b64f89a-176c-4b61-b9ac-29ede63e78b7"):
    response = TemplateResponse.objects.get(id=responseid)
    if response is not None:
        nodes = []
        num_nodes = TemplateNodeResponse.objects.filter(parent_template_response=response).count()
        for i in range(1, num_nodes+1):
            if TemplateNodeResponse.objects.get(parent_template_response=response, position_in_sequence=i):
                nodes.append(TemplateNodeResponse.objects.get(parent_template_response=response, position_in_sequence=i))
            else:
                break

        return render(request, 'view_response.html', {'response_nodes': nodes, 'response': response})
    else:
        return render(request, 'invalid_response.html')
