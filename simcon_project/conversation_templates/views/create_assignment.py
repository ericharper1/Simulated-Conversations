from django.shortcuts import render
from users.models import CustomUser
from users.models import SubjectLabel
from users.models import Assignment
from conversation_templates.models import ConversationTemplate
from django.views.generic import TemplateView
import json
from django.core import serializers
from django.http import HttpResponse

class CreateAssignmentView(TemplateView):
    def get(self, request):
        stud=CustomUser.objects.all()
        label=SubjectLabel.objects.all()
        template=ConversationTemplate.objects.all()
        student = serializers.serialize("json",stud)
        subLabel = serializers.serialize("json",label)
        template = serializers.serialize("json",template)
        return render(request, 'create_assignment.html', {
            'student': student,
            'subLabel': subLabel,
            'template': template
        })


def add_data(request):
    data=request.POST
    name=data.get('name')
    date=data.get('date')
    students=data.get('stuData')
    templates=data.get('tempData')
    labels=data.get('labelData')
    print(students)

    assignment=Assignment()
    assignment.name=name
    assignment.date_assigned=date
    #assignment.researcher='xingjian@111.com'
    assignment.save()
    #assignment.conversation_templates.add(templates)
    assignment.students.add(students)
    #assignment.subject_labels.add(labels)
    #The researcher is not added because I don't know how to get the researcher information now.
    return HttpResponse(json.dumps({
        'success': 0,
    }))

