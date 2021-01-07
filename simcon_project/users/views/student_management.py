from django.contrib.auth import login, authenticate
from users.forms import SignUpForm, CustomUserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from simcon_project.tokens import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from users.models import Student
from django.core.mail import send_mail


def StudentManagement(request):
    if request.method == "POST":
        if request.POST.get('new_student'):
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate Your Simulated Conversation account'
                message = render_to_string('account_activation_email.html', {
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': PasswordResetTokenGenerator.make_token(user),
                })
                email = form.cleaned_data.get('new_student')
                send_mail('testing!','test 12 test 12' , 'TEST.DUMMY.SIM.CON@gmail.com', [email], fail_silently= False)

                #user = authenticate(email=email, is_researcher = False)
                #login(request, user)
            #savest = student()
            #savest.email = request.POST.get('new_student')
            #savest.save()
            return render(request, 'student_management.html')
        if request.POST.get('new_label'):
            #savefldr = SubjectLabel()
            #savefldr.label_name=request.POST.get('new_label')
            #savefldr.save()
            return render(request, 'student_management.html')
    else:
        return render(request, 'student_management.html')


