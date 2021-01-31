from django.contrib.auth.decorators import user_passes_test
from users.views.student_home import is_student
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render


@user_passes_test(is_student)
def student_settings_view(request):
    """
    Settings view for students and researchers (non-staff)
    :param request:
    :return:
    """
    change_password_form = change_password(request)

    return render(request, 'student_settings_view.html', {
        'change_password_form': change_password_form,
    })


@user_passes_test(is_student)
def change_password(request):
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
