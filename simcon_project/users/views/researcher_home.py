from django.shortcuts import render

def ResearcherView(request):
    return render(request, 'researcher_view.html')