from users.forms import SendEmail, NewLabel
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from users.models import Student, Researcher
from django.core.mail import send_mail
from users.models import SubjectLabel
import django_tables2 as tables
from django_tables2.config import RequestConfig
from django.contrib import messages


class StudentList(tables.Table):  #collects info from students to display on the table
    first_name = tables.Column(verbose_name='First Name', accessor='students__first_name')
    last_name = tables.Column(verbose_name='Last Name', accessor='students__last_name')
    email = tables.Column(verbose_name='Email', accessor='students__email')
    registered = tables.Column(verbose_name='Registered', accessor='students__registered')


class LabelList(tables.Table):  #collects the table names
    label_name = tables.Column(linkify={"viewname": "StudentManagement", "args": [tables.A("label_name")]},
                               accessor='label_name', verbose_name='Label Name')


def StudentManagement(request, name="All Students"):
    # gets current researcher for use later
    added_by = Researcher.objects.get(email=request.user)

    #if the label with label_nam = name is not found load default of All Students
    if not SubjectLabel.objects.filter(label_name=name, researcher=added_by):
        name = "All Students"

    #if the table for All Students is deleted or does not exist, make it and add all students the resercher
    # has added and add them to it.
    if not SubjectLabel.objects.filter(label_name='All Students', researcher=added_by):
        test = SubjectLabel().create_label('All Students', added_by)
        all_students = Student.objects.filter(added_by=added_by, is_active=True)
        for stud in all_students:
            test.students.add(stud)

    #creates the table for the labels
    lbl_contents = SubjectLabel.objects.filter(researcher=added_by).values(
        'label_name')
    label_table = LabelList(lbl_contents, prefix="1-")
    RequestConfig(request, paginate={"per_page": 10}).configure(label_table)

    #creates the table for the students in current label
    stu_contents = SubjectLabel.objects.filter(label_name=name).values(
            'students__first_name',
            'students__last_name',
            'students__email',
            'students__registered')
    student_table = StudentList(stu_contents, prefix="2-")
    RequestConfig(request, paginate={"per_page": 10}).configure(student_table)

    #if researcher presses a submit button
    if request.method == "POST":
        if request.POST.get('student_email'):  #create new student
            form = SendEmail(request.POST)

            if form.is_valid():
                new = form.cleaned_data.get('new')
                email = form.cleaned_data.get('student_email')

                if new:
                    #creates a student with blank fist and last names, then the password is set to unusable
                    first_name = ""
                    last_name = ""
                    password = ""
                    user = Student.objects.create(email=email, first_name=first_name, last_name=last_name, password=password, added_by=added_by, )
                    user.set_unusable_password()

                    #adds student to current label and/or the All Students label
                    label = SubjectLabel.objects.get(label_name=name, researcher=added_by)
                    label.students.add(user)
                    if not name == "All Students":
                        label = SubjectLabel.objects.get(label_name="All Students", researcher=added_by)
                        label.students.add(user)

                    #collects the current domain of the website and the users uid
                    current_site = get_current_site(request)
                    site = current_site.domain
                    uid = urlsafe_base64_encode(force_bytes(user.pk))

                    #creates the subject and message content for the emails
                    subject = 'Activate Your Simulated conversations account'
                    message = 'Hi, \nPlease register here: \nhttp://' + site + '/user-registration/'\
                              + uid + '\n'

                    #sends the email
                    send_mail(subject, message, 'simulated.conversation@mail.com', [email], fail_silently=False)

                else:
                    # checks to make sure user exists
                    if Student.objects.filter(email=email):

                        # adds student to current label
                        user = Student.objects.get(email=email)
                        label = SubjectLabel.objects.get(label_name=name, researcher=added_by)
                        label.students.add(user)

                    else:
                        messages.error(request, 'Student does not already exist',
                                       fail_silently=False)
        if request.POST.get('label_name'):  #create new label
            savefldr = NewLabel(request.POST)
            if savefldr.is_valid():
                label_name = savefldr.cleaned_data.get("label_name")

                #if the label does not already exist, create it
                if not SubjectLabel.objects.filter(label_name=label_name, researcher=added_by):
                    SubjectLabel().create_label(label_name, added_by)
                else:
                    messages.error(request, 'Label name already exists',
                                   fail_silently=False)

    return render(request, 'student_management.html',  {"name":name, "form": SendEmail(), "form2": NewLabel(),
                                                        'stu_table': student_table, 'lbl_table': label_table})
