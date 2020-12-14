from django.shortcuts import render

def TemplateManagementView(request):
    return render(request, 'template_management.html')