from django.contrib.auth import get_user_model
from .researcher_home import ResearcherView
from .student_home import StudentView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def RedirectFromLogin(request):
    user = get_user_model()
    if user.get_is_researcher(request.user):
        return HttpResponseRedirect('/researcher-view')
    else:
        return HttpResponseRedirect('/student-view')



