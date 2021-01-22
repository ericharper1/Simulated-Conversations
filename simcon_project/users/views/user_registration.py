from django.shortcuts import render, redirect
from users.models import Student
from django.contrib.auth import login
from users.forms import NewStudentCreationForm
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


def UserRegistration(request, uidb64, token):
        if request.method == "POST":
                form = NewStudentCreationForm(request.POST)

                if form.is_valid():
                        password1 = form.cleaned_data.get('password1')
                        password2 = form.cleaned_data.get('password2')

                        if password1 == password2:
                                email = form.cleaned_data.get('email')

                                if Student.objects.filter(email=email, registered=False):
                                        user = Student.objects.get(email=email, registered=False)
                                        #print(default_token_generator.check_token(user, token))

                                        if (uidb64 == urlsafe_base64_encode(force_bytes(user.pk))): #& default_token_generator.check_token(user, token):
                                                user = Student.objects.get(email=email, registered=False)
                                                user.set_password(form.cleaned_data.get('password1'))
                                                user.first_name = form.cleaned_data.get('first_name')
                                                user.last_name = form.cleaned_data.get('last_name')
                                                user.registered = True
                                                user.save()
                                                login(request, user)
                                                return redirect('/student-view/')
                                        else:
                                                messages.error(request, 'Please use link provided in email, and make '
                                                                        'sure to enter that email in confirm email',
                                                               fail_silently=False)
                                else:
                                        if Student.objects.filter(email=email, registered=True):
                                                messages.error(request, 'Account already created', fail_silently=False)
                                        else:
                                                messages.error(request, 'Invalid email address, please enter the email '
                                                                        'address that you received the email at.',
                                                               fail_silently=False)


                        else:
                                messages.error(request, 'passwords do not match', fail_silently=False)
                else:
                        messages.error(request, 'Please fill out form completely', fail_silently=False)

        return render(request, 'user_registration.html', {"form": NewStudentCreationForm()})
