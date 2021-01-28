from django.shortcuts import render
from conversation_templates.models import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required(login_url="/accounts/login/")
def ResearcherView(request):
    responseTable = TemplateResponse.objects.all()
    if request.method == "POST":
        items_to_delete = request.POST.getlist('delete_items')
        responseTable.filter(pk__in=items_to_delete).delete()
    paginator = Paginator(responseTable, 10)
    pageNumber = request.GET.get('page')
    pageObject = paginator.get_page(pageNumber)
    return render(request, 'researcher_view.html', locals())
