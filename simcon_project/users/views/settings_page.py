from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from users.forms import AddResearcherForm
from users.models import Researcher


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
            return PasswordChangeForm(request.user)
        else:
            messages.error(request, 'Please correct the error below.')
            return PasswordChangeForm(request.user)
    else:
        return PasswordChangeForm(request.user)


@login_required
def AddResearcher(request):
    """
    Displays and validates the AddResearcher form. If AddResearcher form is valid, an account registration email is
        generated and sent to the email address specified in the form. That email will contain a link
        for the user to register their account.
    :param request:
    :return:
    """
    if request.method == 'POST':
        add_researcher_form = AddResearcherForm(request.POST)
        if add_researcher_form.is_valid():
            email_address = add_researcher_form.cleaned_data.get('email')
            first_name = add_researcher_form.cleaned_data.get('first_name')
            last_name = add_researcher_form.cleaned_data.get('last_name')
            user = Researcher.objects.create(email=email_address, first_name=first_name, last_name=last_name)
            user.set_unusable_password()
            current_site = get_current_site(request)
            subject = 'Activate Your Simulated Conversations account'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            site = current_site.domain
            message = 'Hi, \nPlease register here: \nhttp://' + site + '/user-registration/' \
                      + uid + '/' + token + '\n'
            send_mail(subject, message, 'simulated.conversation@mail.com', [email_address], fail_silently=False)
            messages.success(request, 'A link to register has been sent to the researcher\'s email provided.')
            return AddResearcherForm()
        else:
            messages.error(request, 'Please correct the error below.')
            return AddResearcherForm()
    else:
        return AddResearcherForm()
