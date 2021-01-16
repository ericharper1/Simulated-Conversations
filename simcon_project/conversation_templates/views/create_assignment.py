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

def add_data(request):
    data=request.POST
    name=data.get('name')
    date=data.get('date')
    researcher=data.get('researcher')
    students=data.get('stuData')
    templates=data.get('tempData')
    labels=data.get('labelData')

    students=decode(students)
    templates=decode(templates)
    labels=decode(labels)

    assignment=Assignment()
    assignment.name=name
    assignment.date_assigned=date
    researcher=Researcher.objects.get(email=researcher)
    assignment.researcher=researcher
    assignment.save()
    for stu in students:
        stuTmp=Student.objects.get(email=stu)
        assignment.students.add(stuTmp)

    for temp in templates:
        tempList=temp.split('--')
        name=tempList[0]
        date=tempList[1]
        tempTmp=ConversationTemplate.objects.get(name=name,creation_date=date)
        assignment.conversation_templates.add(tempTmp)

    if len(labels)!=0:
        if len(labels)==1 and labels[0]!='':
            for label in labels:
                labelTmp=SubjectLabel.objects.get(label_name=label)
                assignment.subject_labels.add(labelTmp)

    return HttpResponse(json.dumps({
        'success': 0,
    }))

