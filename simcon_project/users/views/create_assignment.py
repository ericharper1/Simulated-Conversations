from django.shortcuts import render
from users.models import SubjectLabel, Assignment, Student, Researcher, Email
from conversation_templates.models import ConversationTemplate
from django.views.generic import TemplateView
from django.core import serializers
from django.http import HttpResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from tzlocal import get_localzone
from django.contrib.auth.decorators import user_passes_test
from users.views.researcher_home import is_researcher
import json
import datetime


class CreateAssignmentView(TemplateView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        curResearcher = request.user

        stud = Student.objects.all().filter(added_by=curResearcher).values('email', 'first_name','last_name','is_active')
        label = SubjectLabel.objects.all().filter(researcher=curResearcher)
        template = ConversationTemplate.objects.all().filter(researcher=curResearcher)

        student = json.dumps(list(stud))
        subLabel = serializers.serialize("json",label)
        template = serializers.serialize("json",template)

        return render(request, 'create_assignment.html', {
            'student': student,
            'subLabel': subLabel,
            'template': template,
        })


# Transfer string type list to list type
def decode(str):
    if str[0] != '[':
        print("Decode failed. The data is not a list type.")
        return
    temp = str[1:-1]
    temp = temp.split(',')
    listTmp = []
    for t in temp:
        t = t[1:-1]
        listTmp.append(t)
    return listTmp


def sendMail(subject, msg, recipient, email_address):
    send_mail(subject, msg, email_address, recipient, fail_silently=False)


# Determine if data is empty.
def isNull(data):
    if len(data)==0 or (len(data)==1 and data[0]==''):
        return True
    return False


@user_passes_test(is_researcher)
def add_assignment(request):
    # Error signs and error messages.
    errMsg = ''
    success = 0

    # Get raw data
    data = request.POST
    name = data.get('name')
    assign_now = data.get('assign_now')
    date = data.get('date')
    researcher = request.user
    students = data.get('stuData')
    templates = data.get('tempData')
    labels = data.get('labelData')

    # Transfer string type list to list type
    students = decode(students)
    templates = decode(templates)
    labels = decode(labels)

    # Verify date
    datetime_now = datetime.datetime.now(get_localzone())
    if assign_now is False:
        sched_datetime = datetime_now
    else:
        sched_datetime = get_localzone().localize(datetime.datetime.strptime(date, "%m/%d/%Y %I:%M %p"))
    if sched_datetime < datetime_now:
        success = 1
        errMsg = errMsg+'The assignment start cannot be before now.\n\n'

    # Determine if students, labels, and templates are empty.
    stuIsNull = isNull(students)
    labelIsNull = isNull(labels)
    tempIsNull = isNull(templates)

    # Save the data that can be directly assigned to assignment.
    assignment = Assignment()
    assignment.name = name
    assignment.date_assigned = sched_datetime
    researcher = Researcher.objects.get(email=researcher)
    assignment.researcher = researcher
    assignment.save()

    # Assign student information to assignment,
    # and judge whether there is an error that both students and labels are empty.
    # Also check if chosen labels have any students in them
    if stuIsNull and labelIsNull:
        success = 1
        errMsg = errMsg+'Either students or labels must not be empty.\n\n'
    labelStudents = Student.objects.filter(labels__label_name__in=labels)
    if stuIsNull and not labelIsNull:
        if stuIsNull and labelStudents.count() <= 0:
            success = 1
            errMsg = errMsg + 'The chosen label(s) does not contain any students.\n\n'
    if not stuIsNull:
        for stu in students:
            stuTmp = Student.objects.get(email=stu)
            assignment.students.add(stuTmp)
    if not labelIsNull:
        for students in labelStudents:
            stuTmp = Student.objects.get(email=students.email)
            assignment.students.add(stuTmp)
        # Assign label information to assignment
        for label in labels:
            labelTmp = SubjectLabel.objects.get(label_name=label)
            assignment.subject_labels.add(labelTmp)

    # Assign template information to assignment
    if tempIsNull:
        success = 1
        errMsg = errMsg+'Template must not be empty.\n\n'
    else:
        for temp in templates:
            tempList = temp.split('--')
            tempName = tempList[0]
            tempDate = tempList[1]
            tempTmp = ConversationTemplate.objects.get(name=tempName, creation_date=tempDate)
            assignment.conversation_templates.add(tempTmp)


    subject='Simulated Conversation Assignment Update'
    msg = 'You received this email because you have a new assignment: '+name+'. Please check the assignment page.'
    #when an error occurs, there is no need to add this task to the schedule.
    if success == 0:
        if assign_now is False:
            print(assign_now)
            sendMail(subject, msg, students, 'simcon.dev@gmail.com')
        else:
            email = Email(subject=subject, message=msg, assignment=assignment)
            email.save()
    else:
        assignment.delete()

    return HttpResponse(json.dumps({
        'success': success,
        'msg': errMsg,
    }))

