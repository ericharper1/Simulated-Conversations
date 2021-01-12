from django.contrib.auth import login, authenticate
from users.forms import SendEmail, NewLabel
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
from users.models import SubjectLabel


def StudentManagement(request):
    if request.method == "POST":
        if request.POST.get('student_email'):
            form = SendEmail(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('student_email')
                send_mail('testing!', 'test 12 test 12', 'TEST.DUMMY.SIM.CON@gmail.com', [email])

                return render(request, 'student_management.html', {"form": SendEmail(), "form2": NewLabel()})

            else:
                return render(request, 'student_management.html', {"form": SendEmail(), "form2": NewLabel()})
        if request.POST.get('label_name'):
            savefldr = NewLabel(request.POST)
            if savefldr.is_valid():
                label_name = savefldr.cleaned_data.get("label_name")
                new_folder = SubjectLabel
                new_folder.create_label(self, 'label_name', )
                new_folder.save()
                return render(request, 'student_management.html', {"form": SendEmail(), "form2": NewLabel()})
            else:
                return render(request, 'student_management.html', {"form": SendEmail(), "form2": NewLabel()})
        else:
            return render(request, 'student_management.html', {"form": SendEmail(), "form2": NewLabel()})
    else:
        return render(request, 'student_management.html', {"form": SendEmail(), "form2": NewLabel()})


