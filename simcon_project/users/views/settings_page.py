from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from users.forms import AddResearcherForm


@login_required
def SettingsView(request):
    """
    This determines if the user is an admin (staff) or not then displays the appropriate view.
    :param request: HttpRequest used to determine what type of user is accessing view (admin/staff or not)
    :return: the HttpRequest object that is returned by the Admin or Standard Settings Views.
    """
    user = get_user_model()
    if user.get_is_staff(request.user):
        return AdminSettingsView(request)
    else:
        return StandardSettingsView(request)


@login_required
def StandardSettingsView(request):
    """
    Settings view for students and researchers (non-staff)
    :param request:
    :return:
    """
    change_password_form = ChangePassword(request)
    add_researcher_form = None

    return render(request, 'settings_view.html', {
        'change_password_form': change_password_form,
        'add_researcher_form': add_researcher_form
    })


@login_required
def AdminSettingsView(request):
    """
    Settings view for just the admin(s) (staff)
    :param request:
    :return:
    """
    change_password_form = ChangePassword(request)
    add_researcher_form = AddResearcher(request)

    return render(request, 'settings_view.html', {
        'change_password_form': change_password_form,
        'add_researcher_form': add_researcher_form
    })


@login_required
def ChangePassword(request):
    """
    Displays and validates Django default PasswordChangeForm
    :param request:
    :return:
    """
    if request.method == 'POST':
        change_password_form = PasswordChangeForm(request.user, request.POST)
        if change_password_form.is_valid():
            user = change_password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        change_password_form = PasswordChangeForm(request.user)
        return change_password_form


@login_required
def AddResearcher(request):
    """
    Displays and validates the AddResearcher form.
    :param request:
    :return:
    """
    add_researcher_form = AddResearcherForm
    if request.method == 'POST':
        if add_researcher_form.is_valid():
            messages.success(request, 'A link to register has been sent to the researcher\'s email provided.')
            return redirect('settings/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        return add_researcher_form
