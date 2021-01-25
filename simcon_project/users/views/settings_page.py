from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
import django_tables2 as tables
from users.forms import AddResearcherForm, DeleteResearchersForm
from users.models import Researcher


class ResearcherTable(tables.Table):
    """
    Table of researchers showing their names and emails.
    first_name is the first name of the researcher.
    last_name is the last name of the researcher.
    email_address is the email address of the researcher used for account creation.
    """
    """
    class Meta:
        model = Researcher
        fields = ('first_name', 'last_name', 'email')
    """
    first_name = tables.Column(accessor='first_name')
    last_name = tables.Column(accessor='last_name')
    email_address = tables.Column(accessor='email')
    delete = tables.TemplateColumn('<input type="checkbox" value="{{ record.email }}" />', verbose_name='Delete?')


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
    researchers_table = None
    delete_researchers_form = None
    add_researcher_form = None

    return render(request, 'settings_view.html', {
        'change_password_form': change_password_form,
        'researchers_table': researchers_table,
        'delete_researchers_form': delete_researchers_form,
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
    researchers_table = GetCurrentResearchers(request)
    delete_researchers_form = DeleteSelectedResearchers(request)
    add_researcher_form = AddResearcher(request)

    return render(request, 'settings_view.html', {
        'change_password_form': change_password_form,
        'researchers_table': researchers_table,
        'delete_researchers_form': delete_researchers_form,
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
def GetCurrentResearchers(request):
    """
    Queries database for all researchers and creates django_table showing their names and emails.
    :param request:
    :return:
    """
    researchers = Researcher.objects.all()
    researchers_table = ResearcherTable(researchers)
    researchers_table.paginate(page=request.GET.get("page", 1), per_page=10)
    return researchers_table


@login_required
def DeleteSelectedResearchers(request):
    """
    If any researchers are selected in researchers_table, this will ask the user to confirm that they
    want to remove them from the database. It displays count of researchers selected during confirmation.
    :param request:
    :return:
    """
    if request.method == 'POST':
        delete_researchers_form = DeleteResearchersForm(request.POST)
        if delete_researchers_form.is_valid():
            email_address = delete_researchers_form.cleaned_data.get('email')
            print(email_address)
            user = Researcher.objects.filter(email=email_address).delete()
            return DeleteResearchersForm()
        else:
            messages.error(request, 'No researchers have been selected.')
            return DeleteResearchersForm()
    else:
        return DeleteResearchersForm()



@login_required
def AddResearcher(request):
    """
    Creates and validates the AddResearcher form. If AddResearcher form is valid, an account registration email is
        generated and sent to the email address specified in the form. That email will contain a link
        for the user to register their account.
    :param request:
    :return: the form to add new researchers.
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
