from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def Home(request):    
    return render(request, 'Home.html')

def Login(request):
    return render(request, 'Login.html')

def ResearcherView(request):
    return render(request, 'ResearcherView.html')

def StudentView(request):
    return render(request, 'StudentView.html')