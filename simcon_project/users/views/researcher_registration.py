from django.shortcuts import render, redirect
from users.models import Researcher
from django.contrib.auth import login
from users.forms import NewResearcherCreationForm
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def ResearcherRegistration(request, uidb64, token):
    """
    This displays a form for the researcher to confirm their account details entered in by the admin
    and to set their password. Sends user to the login page
    :param request:
    :param uidb64:
    :param token: necessary for function to be called correctly. can we remove/change this?
    :return: html page containing form for researcher to register their new account.
    """
    if request.method == "POST":
        form = NewResearcherCreationForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            if password1 == password2:
                email = form.cleaned_data.get('email')
                if Researcher.objects.filter(email=email, registered=False):
                    user = Researcher.objects.get(email=email, registered=False)
                    if uidb64 == urlsafe_base64_encode(force_bytes(user.pk)):
                        user = Researcher.objects.get(email=email, registered=False)
                        user.set_password(form.cleaned_data.get('password1'))
                        user.first_name = form.cleaned_data.get('first_name')
                        user.last_name = form.cleaned_data.get('last_name')
                        user.registered = True
                        user.save()
                        login(request, user)
                        return redirect('Login')
                    else:
                        messages.error(request, 'Please use the link provided in the email and make '
                                                'sure to enter the same email address where the link was originally '
                                                'sent.',
                                       fail_silently=False)
                else:
                    if Researcher.objects.filter(email=email, registered=True):
                        messages.error(request, 'Account already created', fail_silently=False)
                    else:
                        messages.error(request, 'Invalid email address. Please enter the email '
                                                'address that you received the email at.',
                                       fail_silently=False)
            else:
                messages.error(request, 'The passwords you entered do not match.', fail_silently=False)
        else:
            messages.error(request, 'Please fill out the form completely.', fail_silently=False)
    return render(request, 'researcher_registration.html', {"form": NewResearcherCreationForm()})
