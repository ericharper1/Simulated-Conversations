from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Assignment
import django_tables2 as tables


class StudentHomeTable(tables.Table):
    """
    Table of assigned conversation templates for a given student.
    name is the name of the template assigned.
    date_assigned is the date that template was assigned.
    completion_date is the date the template was last completed by the student or is null.
    """
    name = tables.Column(linkify={"viewname": "TemplateStartView", "args": [tables.A("conversation_templates__id")]},
                         accessor='conversation_templates__name',
                         verbose_name='Template Name')
    date_assigned = tables.Column(verbose_name='Date Assigned')
    completion_date = tables.Column(accessor='conversation_templates__template_responses__completion_date',
                                    verbose_name='Last Response')


@login_required
def StudentView(request):
    """
    Queries database for one student's assigned templates, the date they were assigned, the date the student last
        completed a template (if they have completed it, otherwise null), and the id of the template to later create
        a unique URL.
    :param request: HttpRequest containing user id needed to pull one student's assigned templates.
    :return: render returns an HttpResponse object that combines the student_view with the assigned templates table
    """
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
