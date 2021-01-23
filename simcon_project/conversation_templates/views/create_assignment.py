from django.shortcuts import render
from users.models import SubjectLabel
from users.models import Assignment
from users.models import Student
from users.models import Researcher
from conversation_templates.models import ConversationTemplate
from django.views.generic import TemplateView
import json
from django.core import serializers
from django.http import HttpResponse
from django.core.mail import send_mail
from apscheduler.schedulers.background import BackgroundScheduler
from tzlocal import get_localzone


class CreateAssignmentView(TemplateView):
    def get(self, request):
        stud=Student.objects.all().values('email', 'first_name','last_name','is_active')
        label=SubjectLabel.objects.all()
        template=ConversationTemplate.objects.all()
        researchers=Researcher.objects.all().values('email')

        student=json.dumps(list(stud))
        researcher=json.dumps(list(researchers))
        subLabel = serializers.serialize("json",label)
        template = serializers.serialize("json",template)

        return render(request, 'create_assignment.html', {
            'student': student,
            'subLabel': subLabel,
            'template': template,
            'researcher': researcher
        })

#Transfer string type list to list type
def decode(str):
    if str[0]!='[':
        print("Decode failed. The data is not a list type.")
        return
    temp=str[1:-1]
    temp=temp.split(',')
    listTmp=[]
    for t in temp:
        t=t[1:-1]
        listTmp.append(t)
    return listTmp

def sendMail(subject, msg, recipient, researcher):
    send_mail(subject,msg,researcher,recipient,fail_silently=False)

#Determine if data is empty.
def isNull(data):
    if len(data)!=0:
        if len(data)==1:
            if data[0]!='':
                return False
            return True
        return False
    return True

def add_data(request):
    #Error signs and error messages.
    errMsg=''
    success=0

    #Get raw data
    data=request.POST
    name=data.get('name')
    date=data.get('date')
    researcher=data.get('researcher')
    students=data.get('stuData')
    templates=data.get('tempData')
    labels=data.get('labelData')

    #Transfer string type list to list type
    students=decode(students)
    templates=decode(templates)
    labels=decode(labels)

    #Save the data that can be directly assigned to assignment.
    assignment=Assignment()
    assignment.name=name
    assignment.date_assigned=date
    researcher=Researcher.objects.get(email=researcher)
    assignment.researcher=researcher
    assignment.save()

    #Determine if students, labels, and templates are empty.
    stuIsNull=isNull(students)
    labelIsNull=isNull(labels)
    tempIsNull=isNull(templates)

    #Assign student information to assignment,
    #and judge whether there is an error that both students and labels are empty.
    if stuIsNull:
        if labelIsNull:
            success=1
            errMsg='One of the students or labels must not be empty.'
    else:
        for stu in students:
            stuTmp=Student.objects.get(email=stu)
            assignment.students.add(stuTmp)

    #Assign template information to assignment
    if tempIsNull:
        success=1
        errMsg='Template must not be empty.'
    else:
        for temp in templates:
            tempList=temp.split('--')
            tempName=tempList[0]
            tempDate=tempList[1]
            tempTmp=ConversationTemplate.objects.get(name=tempName,creation_date=tempDate)
            assignment.conversation_templates.add(tempTmp)

    ##Assign label information to assignment
    if not labelIsNull:
        for label in labels:
            labelTmp=SubjectLabel.objects.get(label_name=label)
            assignment.subject_labels.add(labelTmp)

    #Send email
    job_defaults = { 'max_instances': 20 }
    tz = get_localzone()
    sched = BackgroundScheduler(timezone=tz, job_defaults=job_defaults)

    subject='You received a new assignment.'
    msg='You received this email because you have a new assignment: '+name+'. Please check the assignment page.'
    schedId='Assignment--'+name
    #run_date='2021-01-22 18:35:00'
    sched.add_job(sendMail, trigger='date', id=schedId, run_date=date, args=(subject, msg, students, researcher))
    sched.start()

    # print(success)
    # print(errMsg)
    # print(repr(stuIsNull)+"  "+repr(labelIsNull)+"  "+repr(tempIsNull))
    return HttpResponse(json.dumps({
        'success': success,
        'msg': errMsg,
    }))

