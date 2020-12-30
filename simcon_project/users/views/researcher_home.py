from django.shortcuts import render

def ResearcherView(request):
    return render(request, 'users/researcher_view.html')