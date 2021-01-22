from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def ResearcherUserView(request):
    return render(request, 'researcher_user_view.html')

