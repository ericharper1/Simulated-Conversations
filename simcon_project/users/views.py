from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import CustomUser


# Create your views here.
def Home(request):
    return render(request, 'home.html')


def Login(request):
    return render(request, 'login.html')


def RedirectToView(request):

    user = get_user_model()

    if user.get_is_researcher(request.user) == True:
        return ResearcherView(request)
    else:
        return StudentView(request)

def ResearcherView(request):
    return render(request, 'researcher_view.html')


def StudentView(request):
    return render(request, 'student_view.html')