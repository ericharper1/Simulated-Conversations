from django.shortcuts import render
from conversation_templates.models import TemplateResponse, TemplateNodeResponse


def ViewResponse(request, responseID):
    response = TemplateResponse.objects.get(responseID)
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
