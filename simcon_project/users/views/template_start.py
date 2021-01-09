from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def TemplateStartView(request, name=None):
    return render(request, 'template_start_view.html', {'name': name})
