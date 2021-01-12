from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def ResearcherView(request):
    return render(request, 'researcher_view.html')