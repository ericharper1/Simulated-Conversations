from django.shortcuts import render
import django_tables2 as tables
from django_tables2.config import RequestConfig
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy
from users.views.researcher_home import is_researcher
from users.models import Assignment, Researcher
from conversation_templates.models import ConversationTemplate, TemplateResponse
from bootstrap_modal_forms.generic import BSModalDeleteView


class AssignmentsTable(tables.Table):
    name = tables.Column(verbose_name='Assignment Name', accessor='name')
    date_assigned = tables.Column(verbose_name='Date Assigned', accessor='date_assigned')
    view_templates = tables.TemplateColumn(verbose_name='',
                                           template_name='assignment_management/view_templates_button.html')
    completion = tables.Column(verbose_name='% Students Completed', accessor='completion')
    delete = tables.TemplateColumn(verbose_name='', template_name='assignment_management/delete_ass_button.html')


class TemplatesContainedTable(tables.Table):
    name = tables.Column(verbose_name='Template Name', accessor='name') # make link to template management
    description = tables.Column(verbose_name='Description', accessor='description')
    creation_date = tables.Column(verbose_name='Creation Date', accessor='creation_date')


class AssignmentDeleteView(BSModalDeleteView):
    """
    Deletes an assignment. Confirmation modal pops up to make sure
    the user wants to delete.
    """
    model = Assignment
    template_name = 'assignment_management/assignment_delete_modal.html'
    success_message = 'Success: Assignment was deleted.'
    success_url = reverse_lazy('ass-management:main')

    def get(self, request, *args, **kwargs):
        """
        Override post to send name of assignment that
        will be removed as context to the template
        """
        super().get(request, *args, **kwargs)
        assignment = Assignment.objects.get(pk=self.kwargs['pk'])
        context = {"assignment": assignment}
        return render(request, self.template_name, context)


@user_passes_test(is_researcher)
def assignment_management_view(request):
    assignment_rows = []
    researcher = Researcher.objects.get(id=request.user.id)
    assignments = Assignment.objects.filter(researcher=researcher)

    for assignment in assignments:
        total_assigned_templates = ConversationTemplate.objects.filter(assignments=assignment).count() * \
                                   assignment.students.count()
        templates = ConversationTemplate.objects.filter(assignments=assignment)
        total_completed_templates = TemplateResponse.objects.filter(assignment=assignment,
                                                                    template__in=templates).\
                                                            values('student').\
                                                            distinct().count()
        completion_percent = total_completed_templates / total_assigned_templates

        row_data = {}
        row_data.update({"id": assignment.id,
                        "name": assignment.name,
                         "date_assigned": assignment.date_assigned,
                         "completion": completion_percent})
        assignment_rows.append(row_data)

    assignments_table = AssignmentsTable(assignment_rows)
    RequestConfig(request, paginate={"page": 10}).configure(assignments_table)
    return render(request, 'assignment_management/main_view.html', {'table': assignments_table})


@user_passes_test(is_researcher)
def view_templates(request, pk):
    assignment = Assignment.objects.get(pk=pk)
    templates = ConversationTemplate.objects.filter(assignments=assignment)
    templates_contained_table = TemplatesContainedTable(templates)
    RequestConfig(request, paginate={"per_page": 10}).configure(templates_contained_table)
    return render(request, 'assignment_management/view_templates_modal.html', {'table': templates_contained_table})
