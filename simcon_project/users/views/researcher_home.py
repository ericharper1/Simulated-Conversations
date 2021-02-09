from django.shortcuts import render
from django.db.models import Q
from conversation_templates.models import TemplateResponse
from django.contrib.auth.decorators import user_passes_test
import django_tables2 as tables
from django_tables2 import RequestConfig


class ResponseTable(tables.Table):
    name = tables.columns.Column(accessor="student.get_full_name")
    response = tables.TemplateColumn(
        '''<a class="btn btn-info btn-sm" href="{% url 'view-response' record.id %}">View</a>''')
    delete = tables.TemplateColumn(
        '''<a class="btn btn-danger" href="{% url 'delete-response' record.id %}"  >Delete</a>''')

    class Meta:
        attrs = {'class': 'table table-sm', 'id': 'response-table'}
        model = TemplateResponse
        fields = ['template', 'name', 'completion_date', 'feedback']


def is_researcher(user):
    return user.is_authenticated and user.get_is_researcher()


@user_passes_test(is_researcher)
def researcher_view(request):
    responses = TemplateResponse.objects.filter(
        template__researcher__email=request.user)
    filtered_responses = filter_search(request, responses)

    if filtered_responses:
        response_table = ResponseTable(filtered_responses)
        RequestConfig(request, paginate={"per_page": 5}).configure(
            response_table)
    else:
        response_table = None

    context = {'responseTable': response_table}

    return render(request, 'researcher_view.html', context)


def filter_search(request, responses):
    if 'searchParam' in request.GET:
        param = request.GET['searchParam']
        filter_fields = Q(student__first_name__contains=param) | Q(student__last_name__contains=param) | \
            Q(template__name__contains=param) | \
            Q(assignment__subject_labels__label_name__contains=param)
        responses = responses.filter(filter_fields)

    return responses
