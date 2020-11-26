from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser


# Create your views here.
def Home(request):
    return render(request, 'Home.html')


def Login(request):
    return render(request, 'login.html')


def RedirectToView(request):

    # user = str(request.session.get('id_username'))
    user = CustomUser.objects.filter(email=request.GET.get("email"))
    # user = request.get(id_username="student@student.com")

    # email = str(request.GET.get("id_username"))
    return HttpResponse(user)
    # if user.is_researcher == True:
    #     return ResearcherView(request)
    # else:
    #     return StudentView


def ResearcherView(request):
    return render(request, 'ResearcherView.html')


def StudentView(request):
    return render(request, 'StudentView.html')