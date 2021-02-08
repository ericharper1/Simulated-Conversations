from django.shortcuts import render
from django.db.models import Q
from conversation_templates.models import TemplateResponse
from django.contrib.auth.decorators import user_passes_test
from django_tables2 import TemplateColumn, tables, RequestConfig, A


class ResponseTable(tables.Table):
    name = tables.columns.Column(accessor="student.get_full_name")

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
        # Add columns you want the search to apply to here
        filter_fields = Q(student__first_name__contains=param) | Q(student__last_name__contains=param) | \
            Q(template__name__contains=param)
        responses = responses.filter(filter_fields)

    return responses

# @user_passes_test(is_researcher)
# def researcher_view(request):
#    #responseTable = TemplateResponse.objects.all()
#    responseTable = TemplateResponse.objects.filter(
#        template__researcher__email__icontains=request.user.email)
#    print(responseTable)
#    if request.method == "POST":
#        responseTable = TemplateResponse.objects.all()
#        items_to_delete = request.POST.getlist('delete_items')
#        responseTable.filter(pk__in=items_to_delete).delete()
#    if 'searchParam' in request.GET and request.GET['searchParam']:
#        responseTable = TemplateResponse.objects.all()
#        searchParam = request.GET['searchParam']
#        searchResponses = []
#        search1 = TemplateResponse.objects.filter(
#            student__email__icontains=searchParam)
#        searchResponses.append(search1)
#        search2 = TemplateResponse.objects.filter(
#            template__name__icontains=searchParam)
#        searchResponses.append(search2)
#        search3 = TemplateResponse.objects.filter(
#            assignment__subject_labels__label_name__icontains=searchParam)
#        searchResponses.append(search3)
#        print(searchResponses)
#        return render(request, 'researcher_view.html',
#                      {'searchResponses': searchResponses})
#    paginator = Paginator(responseTable, 10)
#    pageNumber = request.GET.get('page')
#    pageObject = paginator.get_page(pageNumber)
#    return render(request, 'researcher_view.html', locals())
