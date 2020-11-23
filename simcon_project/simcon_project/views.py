from django.shortcuts import render
from django.http import HttpResponse
#Views go here

def home(request):
    return render(request, 'home.html')