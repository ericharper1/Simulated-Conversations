from django.contrib.auth import login, authenticate
from users.forms import SendEmail, NewLabel
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from simcon_project.tokens import account_activation_token
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from users.models import Student, Researcher
from django.core.mail import send_mail
from users.models import SubjectLabel
from simcon_project.settings import EMAIL_HOST_USER
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.core.mail import EmailMessage
import uuid


def StudentManagement(request):
    if request.method == "POST":
        if request.POST.get('student_email'):
            form = SendEmail(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('student_email')
                first_name = ""
                last_name = ""
                password = ""
                added_by = Researcher.objects.get(email=request.user)
                user = Student.objects.create(email=email, first_name=first_name, last_name=last_name, password=password, added_by=added_by, )
                user.set_unusable_password()

                current_site = get_current_site(request)
                subject = 'Activate Your Simulated conversations account'
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                site = current_site.domain

                message = 'Hi, \nPlease register here: \nhttp://' + site + '/user-registration/'\
                          + uid + '/' + token + '\n'
                send_mail(subject, message, 'simulated.conversation@mail.com', [email], fail_silently=False)

                return render(request, 'student_management.html', {"form": SendEmail(), "form2": NewLabel()})

            else:
                return render(request, 'student_management.html', {"form": SendEmail(), "form2": NewLabel()})
        if request.POST.get('label_name'):
            savefldr = NewLabel(request.POST)
            if savefldr.is_valid():
                researcher = Researcher.objects.get(email=request.user)
                label_name = savefldr.cleaned_data.get("label_name")

                SubjectLabel().create_label(label_name, researcher)
                #print(label.students.all())


                return render(request, 'student_management.html', {"form": SendEmail(), "form2": NewLabel()})
            else:
                return render(request, 'student_management.html', {"form": SendEmail(), "form2": NewLabel()})
        else:
            return render(request, 'student_management.html', {"form": SendEmail(), "form2": NewLabel()})
    else:
        return render(request, 'student_management.html', {"form": SendEmail(), "form2": NewLabel()})
