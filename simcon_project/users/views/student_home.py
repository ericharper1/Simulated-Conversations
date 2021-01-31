from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Max
from users.models import *
from conversation_templates.models import *
import django_tables2 as tables
from django_tables2 import RequestConfig


def is_student(user):
    return user.is_authenticated and not user.get_is_researcher()


class StudentHomeTable(tables.Table):
    """
    Table of assigned conversation templates for a given student.
    name is the name of the template assigned. links to conversation-start
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
def student_view(request):
    """
    Creates table of the student's assigned templates with links to start new responses.
    :param request:
    :return: student_view.html with table
    """
    assigned_templates = []
    # get the Student object matching logged in student
    student = Student.objects.filter(id=request.user.id)
    # get the assignments for that student
    assignments = Assignment.objects.filter(students=student.first())
    # for each assignment, get all templates contained. Get most recent response by the student for each template
    for assignment in assignments:
        templates_in_assignment = ConversationTemplate.objects.filter(assignments=assignment)
        for template in templates_in_assignment:
            last_response = TemplateResponse.objects.filter(assignment=assignment, template=template,
                                                            student=student.first()).aggregate(Max('completion_date'))
            assigned_template_row = {}
            assigned_template_row.update({"conversation_templates__id": template.id,
                                          "id": assignment.id,
                                          "conversation_templates__name": template.name,
                                          "date_assigned": assignment.date_assigned,
                                          "conversation_templates__template_responses__completion_date":
                                              last_response['completion_date__max']})
            assigned_templates.append(assigned_template_row)
    assigned_templates_table = StudentHomeTable(assigned_templates)
    RequestConfig(request, paginate={"page": 10}).configure(assigned_templates_table)
    return render(request, 'student_view.html', {'table': assigned_templates_table})
