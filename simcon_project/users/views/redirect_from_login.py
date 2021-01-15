from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def RedirectFromLogin(request):
    user = get_user_model()
    if user.get_is_researcher(request.user):
        return HttpResponseRedirect('/researcher-view')
    else:
        return HttpResponseRedirect('/student-view')



