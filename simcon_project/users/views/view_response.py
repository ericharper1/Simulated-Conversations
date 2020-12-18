from django.shortcuts import render


def ViewResponse(request, response=None):
    if response is not None:
        nodes = []
        for node in response.node_responses:
            nodes.append(node)
        return render(request, 'view_response.html', {'response': nodes})
    else:
        return render(request, 'invalid_response.html')
