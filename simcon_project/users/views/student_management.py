from users.forms import SendEmail, NewLabel
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from users.models import Student, Researcher
from django.core.mail import send_mail
from users.models import SubjectLabel
import django_tables2 as tables


class StudentList(tables.Table):
    first_name = tables.Column(verbose_name='First Name', accessor='students__first_name')
    last_name = tables.Column(verbose_name='Last Name', accessor='students__last_name')
    email = tables.Column(verbose_name='Email', accessor='students__email')
    registered = tables.Column(verbose_name='Registered', accessor='students__registered')


class AllStudentList(tables.Table):
    first_name = tables.Column(verbose_name='First Name')
    last_name = tables.Column(verbose_name='Last Name')
    email = tables.Column(verbose_name='Email')
    registered = tables.Column(verbose_name='Registered')


class LabelList(tables.Table):
    label_name = tables.Column(linkify={"viewname": "StudentManagement", "args": [tables.A("label_name")]},
                               accessor='label_name', verbose_name='Label Name')
    students = tables.Column(verbose_name='# of Students')


def StudentManagement(request, name):
    if not SubjectLabel.objects.filter(label_name=name):
        name = 'All_Students'

    lbl_contents = SubjectLabel.objects.filter().values(
        'label_name',
        'students')
    label_table = LabelList(lbl_contents)
    label_table.paginate(page=request.GET.get("page", 1), per_page=10)

    if name != 'All_Students':
        stu_contents = SubjectLabel.objects.filter(label_name=name).values(
            'students__first_name',
            'students__last_name',
            'students__email',
            'students__registered')
        student_table = StudentList(stu_contents)
        student_table.paginate(page=request.GET.get("page", 1), per_page=10)

    else:
        stu_contents = Student.objects.filter(is_active=True, ).values(
            'first_name',
            'last_name',
            'email',
            'registered')
        student_table = AllStudentList(stu_contents)
        student_table.paginate(page=request.GET.get("page", 1), per_page=10)

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

        if request.POST.get('label_name'):
            savefldr = NewLabel(request.POST)
            if savefldr.is_valid():

                researcher = Researcher.objects.get(email=request.user)
                label_name = savefldr.cleaned_data.get("label_name")

                test = SubjectLabel().create_label(label_name, researcher)

                test.students.add(Student.objects.get(email='test1@gmail.com'))

    return render(request, 'student_management.html', {"form": SendEmail(), "form2": NewLabel(), 'stu_table': student_table, 'lbl_table': label_table})
