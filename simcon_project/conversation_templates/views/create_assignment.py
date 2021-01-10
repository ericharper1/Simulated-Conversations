from django.shortcuts import render
from users.models import CustomUser
from django.contrib import messages
from django.views.generic import TemplateView
import json
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators import csrf
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class CreateAssignmentView(TemplateView):
    context = {
        "students": CustomUser.objects.all(),
        "templates": CustomUser.objects.all(),
        "labels": CustomUser.objects.all(),
    }
    def get(self, request):
        stud=CustomUser.objects.all()
        tmpJson = serializers.serialize("json",stud)
        #return HttpResponse(tmpJson, content_type='application/json')
        #tmpObj = json.loads(tmpJson)
        #return render(request, 'create_assignment.html', {'ctx': json.dumps(tmpObj)})
        return render(request, 'create_assignment.html', {'ctx': tmpJson})
        #return JsonResponse(model_to_dict(stud))


def add_data(request):
    data=request.POST
    students=data.get('stuData')
    print(students)
    return HttpResponse(json.dumps({
        'success': 0,
    }))




# def add_stu(request):
#     print(1)
#     if request.POST:
#         print(2)
#         stu=CustomUser.objects.get(email=request.POST['stu_name'])
#         name=stu.first_name+" "+stu.last_name
#         if stu.is_researcher:
#             print('Add failed. This user is a researcher')
#             messages.error(request, 'Add failed. This user is a researcher')
#         if stu.is_staff:
#             print('Add failed. This user is a staff')
#             messages.error(request, 'Add failed. This user is a staff')
#         if stu.is_active:
#             print('Add failed. This user is a not an active user')
#             messages.error(request, 'Add failed. This user is a not an active user')
#         ctx ={}
#         ctx['rlt'] = name
#         print("sucess!")
#         return render_to_response(request, "create_assignment.html", ctx)
#     else:
#         print(3)
#         messages.error(request, 'POST is null!')