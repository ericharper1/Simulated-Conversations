from django.shortcuts import render, redirect
from django.db import models
from users.models import Student, subject_label, CustomUser
from django.contrib.auth import login, authenticate
from users.forms import NewStudentCreationForm
from django.views.generic import CreateView

class temp(CreateView):
        template_name = "user_registration.html"
        form_class = NewStudentCreationForm
        success_url = "student-view/"

def UserRegistration(request):
        if request.method == "POST":
                form = NewStudentCreationForm(request.POST)
                print(request.POST)
                if form.is_valid():
                        print("!")
                        email = form.cleaned_data.get('email')
                        password = form.cleaned_data.get('password1')
                        Student.objects.create_user(email, password)
                        user = authenticate(email=email, password=password)
                        login(request, user)
                        return render(request, 'user_registration.html', {"form": NewStudentCreationForm()})

                else:
                        print(":(")
                        return render(request, 'user_registration.html', {"form": NewStudentCreationForm()})

        else:
                return render(request, 'user_registration.html',{"form": NewStudentCreationForm()})
