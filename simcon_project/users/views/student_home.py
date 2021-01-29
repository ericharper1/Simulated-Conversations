from django.shortcuts import render
from users.models import Assignment
from django.contrib.auth.decorators import user_passes_test
import django_tables2 as tables


def is_student(user):
    return user.is_authenticated and not user.get_is_researcher()


class StudentHomeTable(tables.Table):
    """
    Table of assigned conversation templates for a given student.
    name is the name of the template assigned.
    date_assigned is the date that template was assigned.
    completion_date is the date the template was last completed by the student or is null.
    """
    name = tables.Column(linkify=("conversation-start",
                                  {"ct_id": tables.A("conversation_templates__id"),
                                   "assign_id": tables.A("id")
                                   }),
                         accessor='conversation_templates__name',
                         verbose_name='Template Name')
    date_assigned = tables.Column(verbose_name='Date Assigned')
    completion_date = tables.Column(accessor='conversation_templates__template_responses__completion_date',
                                    verbose_name='Last Response')


@user_passes_test(is_student)
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
            'conversation_templates__id',
            'id'
    )
    template_table = StudentHomeTable(contents)
    template_table.paginate(page=request.GET.get("page", 1), per_page=10)
    return render(request, 'student_view.html', {'table': template_table})
