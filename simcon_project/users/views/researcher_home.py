from django.shortcuts import render
from conversation_templates.models import TemplateResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url="/accounts/login/")
def ResearcherView(request):
    responseTable = TemplateResponse.objects.all()
    return render(request, 'researcher_view.html', locals())

