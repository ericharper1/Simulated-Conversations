from django.shortcuts import render
from users.views.researcher_home import is_researcher
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(is_researcher)
def researcher_user_view(request):
    return render(request, 'researcher_user_view.html')
