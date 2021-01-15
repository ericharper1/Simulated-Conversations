from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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
        response_table.filter(pk__in=items_to_delete).delete()
    paginator = Paginator(response_table, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'researcher_view.html', locals())
