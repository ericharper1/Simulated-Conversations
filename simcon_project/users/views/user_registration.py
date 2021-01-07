from django.shortcuts import render, redirect
from django.db import models
from users.models import student, subject_label
from django.contrib.auth import login, authenticate
#from users.forms import NewStudentCreationForm
from users.forms import CustomUserCreationForm


def UserRegistration(request):
        if request.method == "POST":
                #form = NewStudentCreationForm(request.POST)
                form = CustomUserCreationForm(request.POST)
                if form.is_valid():
                        form.save()
                        email = form.cleaned_data.get('new_student')
                        first_name = form.cleaned_data.get('first_name')
                        last_name = form.cleaned_data.get('last_name')
                        password1 = form.cleaned_data.get('password1')
                        password2 = form.cleaned_data.get('password2')
                        if password1 == password2:
                                user = authenticate(email=email,  password=password1, is_researcher=False, first_name=first_name, last_name=last_name)
                                login(request, user)
                                return redirect(request, 'student_home.html')
        else:
                return render(request, 'user_registration.html')


