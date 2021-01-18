from django.shortcuts import render, redirect
from users.models import Student
from django.contrib.auth import login
from users.forms import NewStudentCreationForm
from django.contrib import messages


def UserRegistration(request, uidb64, token):
        print(uidb64)
        if request.method == "POST":
                form = NewStudentCreationForm(request.POST)
                if form.is_valid():
                        password1 = form.cleaned_data.get('password1')
                        password2 = form.cleaned_data.get('password2')

                        if password1 == password2:
                                email = form.cleaned_data.get('email')

                                if Student.objects.filter(email=email, registered=False):
                                        user = Student.objects.get(email=email, registered=False)
                                        user.set_password(form.cleaned_data.get('password1'))
                                        user.first_name = form.cleaned_data.get('first_name')
                                        user.last_name = form.cleaned_data.get('last_name')
                                        user.registered = True
                                        user.save()
                                        login(request, user)
                                        return redirect('student_home.html')
                                else:
                                        if Student.objects.filter(email=email, registered=True):
                                                messages.error(request, 'Account already created', fail_silently=False)
                                        else:
                                                messages.error(request, 'Invalid email address, please enter the email address '
                                                                'that you received the email at.', fail_silently=False)
                                        return render(request, 'user_registration.html',
                                                      {"form": NewStudentCreationForm()})

                        else:
                                messages.error(request, 'passwords do not match', fail_silently=False)
                                return render(request, 'user_registration.html', {"form": NewStudentCreationForm()})
                else:
                        messages.error(request, 'Please fill out form completely', fail_silently=False)
                        return render(request, 'user_registration.html', {"form": NewStudentCreationForm()})

        else:
                return render(request, 'user_registration.html',{"form": NewStudentCreationForm()})
