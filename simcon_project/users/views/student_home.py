from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.models import Assignment
import django_tables2 as tables


class StudentHomeTable(tables.Table):
    name = tables.Column(linkify=("conversation-start",
                                  {"ct_id": tables.A("conversation_templates__id"),
                                   "assign_id": tables.A("id")
                                   }),
                         accessor='conversation_templates__name',
                         verbose_name='Template Name')
    date_assigned = tables.Column(verbose_name='Date Assigned')
    completion_date = tables.Column(accessor='conversation_templates__template_responses__completion_date',
                                    verbose_name='Last Response')


@login_required(login_url="/accounts/login/")
def StudentView(request):
    contents = Assignment.objects.filter(students=request.user.id)\
        .values(
            'conversation_templates__name',
            'date_assigned',
            'conversation_templates__template_responses__completion_date',
            'conversation_templates__id',
            'id'
    )
    template_table = StudentHomeTable(contents)
    template_table.paginate(page=request.GET.get("page", 1), per_page=10)
    return render(request, 'student_view.html', {'table': template_table})
