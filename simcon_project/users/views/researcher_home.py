from django.shortcuts import render
from conversation_templates.models import TemplateResponse

def ResearcherView(request):
    responseTable = TemplateResponse.objects.all()
    return render(request, 'researcher_view.html', locals())