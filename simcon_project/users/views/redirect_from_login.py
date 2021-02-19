from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
import django.utils.timezone as timezone


def is_authenticated(user):
    return user.is_authenticated


@user_passes_test(is_authenticated)
def redirect_from_login(request):
    user = get_user_model()
    timezone.activate(timezone.get_current_timezone_name())
    if user.get_is_researcher(request.user):
        return HttpResponseRedirect(reverse('researcher-view'))
    else:
        return HttpResponseRedirect(reverse('student-view'))
