from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import *


class StudentHomeTable(tables.Table):
    name = tables.Column(linkify={"viewname": "TemplateStartView", "args": [tables.A("conversation_templates__name")]},
                         accessor='conversation_templates__name',
                         verbose_name='Template Name')
    date_assigned = tables.Column(verbose_name='Date Assigned')
    completion_date = tables.Column(accessor='conversation_templates__template_responses__completion_date',
                                    verbose_name='Last Response')

@login_required
def StudentView(request):
    contents = Assignment.objects.filter(students=request.user.id)\
        .values(
            'conversation_templates__name',
            'date_assigned',
            'conversation_templates__template_responses__completion_date',
            'conversation_templates__id')
    template_table = StudentHomeTable(contents)
    template_table.paginate(page=request.GET.get("page", 1), per_page=10)
    # must pass context as a dictionary
    return render(request, 'student_view.html', {'table': template_table})
