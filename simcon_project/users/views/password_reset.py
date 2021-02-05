from users.forms import SendEmail, PassReset
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from users.models import Student, Researcher
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages


def password_reset(request):

    if request.method == "POST":
            form = PassReset(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                if Student.objects.filter(email=email, is_active=True) or Researcher.objects.filter(email=email, is_active=True):
                    if Student.objects.filter(email=email, is_active=True):
                        user = Student.objects.get(email=email, is_active=True)
                    else:
                        user = Researcher.objects.get(email=email, is_active=True)
                    # collects the current domain of the website and the users uid
                    current_site = get_current_site(request)
                    site = current_site.domain
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token=default_token_generator.make_token(user)

                    # creates the subject and message content for the emails
                    subject = 'Reset Your Simulated conversations account password'
                    message = 'Hi, \nPlease follow this link to reset your password: \nhttp://' + site + \
                              '/password-reset-confirm/' + uid + '/' + token + '/' '\n'

                    # sends the email
                    send_mail(subject, message, 'simulated.conversation@mail.com', [email], fail_silently=False)
                    return redirect('/password-reset/done')
                else:
                    messages.error(request, 'Invalid Email', fail_silently=False)
            else:
                messages.error(request, 'Invalid Email', fail_silently=False)

    return render(request, 'registration/password_reset.html', {"form": PassReset()})