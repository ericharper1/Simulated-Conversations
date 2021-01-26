from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render


@login_required
def StudentSettingsView(request):
    """
    Settings view for students and researchers (non-staff)
    :param request:
    :return:
    """
    change_password_form = ChangePassword(request)

    return render(request, 'StudentSettingsView.html', {
        'change_password_form': change_password_form,
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
            return PasswordChangeForm(request.user)
        else:
            messages.error(request, 'Please correct the error below.')
            return PasswordChangeForm(request.user)
    else:
        return PasswordChangeForm(request.user)
