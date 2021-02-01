from django.shortcuts import render
from conversation_templates.models import TemplateResponse
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator


def is_researcher(user):
    return user.is_authenticated and user.get_is_researcher()


@user_passes_test(is_researcher)
def researcher_view(request):
    response_table = TemplateResponse.objects.all()
    if request.method == "POST":
        items_to_delete = request.POST.getlist('delete_items')
        responseTable.filter(pk__in=items_to_delete).delete()
    if 'searchParam' in request.GET and request.GET['searchParam']:
        searchParam = request.GET['searchParam']
        searchResponses = []
        search1 = TemplateResponse.objects.filter(
            student__email__icontains=searchParam)
        searchResponses.append(search1)
        search2 = TemplateResponse.objects.filter(
            template__name__icontains=searchParam)
        searchResponses.append(search2)
        search3 = TemplateResponse.objects.filter(
            assignment__subject_labels__label_name__icontains=searchParam)
        searchResponses.append(search3)
        return render(request, 'researcher_view.html',
                      {'searchResponses': searchResponses})
    paginator = Paginator(responseTable, 10)
    pageNumber = request.GET.get('page')
    pageObject = paginator.get_page(pageNumber)
    return render(request, 'researcher_view.html', locals())
