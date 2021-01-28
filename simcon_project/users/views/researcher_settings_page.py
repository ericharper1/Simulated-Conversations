from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="/accounts/login/")
def ResearcherSettingsView(request):
    return render(request, 'researcher_settings_view.html')
