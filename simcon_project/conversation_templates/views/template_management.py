from django.views.generic import DeleteView, RedirectView
from django.db.models import Q
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from users.views.researcher_home import is_researcher
from conversation_templates.models import ConversationTemplate, TemplateFolder
from conversation_templates.forms import FolderCreationForm
from users.models import Researcher
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView, BSModalDeleteView
from django_tables2 import TemplateColumn, tables, RequestConfig, A
import re


class FolderTemplateTable(tables.Table):
    """
    Table for showing the templates for a specific folder.
    The "delete" button has been replaced with a "remove button to
    remove a template from the folder.
    """
    buttons = TemplateColumn(verbose_name='', template_name='template_management/buttons_template.html',
                             extra_context={"in_folder": True})
    name = tables.columns.LinkColumn('view-all-responses', args=[A('pk')])

    class Meta:
        attrs = {'class': 'table table-sm', 'id': 'template-table'}
        model = ConversationTemplate
        fields = ['name', 'description', 'creation_date']


class AllTemplateTable(tables.Table):
    """
    Table for showing the templates for a specific folder.
    Only used when all templates are displayed.
    """
    buttons = TemplateColumn(verbose_name='', template_name='template_management/buttons_template.html')
    name = tables.columns.LinkColumn('view-all-responses', args=[A('pk')])

    class Meta:
        attrs = {'class': 'table table-sm', 'id': 'template-table'}
        model = ConversationTemplate
        fields = ['name', 'description', 'creation_date']


class FolderTable(tables.Table):
    """
    Table showing all folders (unique to a researcher in the future)
    """
    name = tables.columns.LinkColumn('management:folder-view', args=[A('pk')])

    class Meta:
        attrs = {'class': 'table table-sm', 'id': 'folder-table'}
        model = TemplateFolder
        fields = ['name']


@user_passes_test(is_researcher)
def main_view(request):
    """
    Main template management view.
    Main contents of the page are the tables showing all templates and folders the researcher has created.
    """
    all_templates = get_templates(request.user)
    templates = filter_templates(request, all_templates)
    if templates:
        template_table = AllTemplateTable(templates, prefix="1-")
        RequestConfig(request, paginate={"per_page": 5}).configure(template_table)
    else:
        template_table = None

    folders = filter_folder(request)
    if folders:
        folder_table = FolderTable(folders, prefix="2-")
        RequestConfig(request, paginate={"per_page": 5}).configure(folder_table)
    else:
        folder_table = None

    context = {
        'templateTable': template_table,
        'folderTable': folder_table,
        'folder_pk': None,
    }

    return render(request, 'template_management/main_view.html', context)


@user_passes_test(is_researcher)
def folder_view(request, pk):
    """
    Main template management view.
    Shows the all folders, but shows only templates belonging to the selected folder
    """
    current_folder = get_object_or_404(TemplateFolder, pk=pk)

    all_templates = current_folder.templates.all()
    templates = filter_templates(request, all_templates)
    if templates:
        template_table = FolderTemplateTable(templates, prefix="1-")
        RequestConfig(request, paginate={"per_page": 5}).configure(template_table)
    else:
        template_table = None

    folders = filter_folder(request)
    folder_table = FolderTable(folders, prefix="2-")

    RequestConfig(request, paginate={"per_page": 5}).configure(folder_table)

    context = {
        'templateTable': template_table,
        'folderTable': folder_table,
        'folder_pk': pk
    }

    return render(request, 'template_management/main_view.html', context)


class RedirectToTemplateCreation(RedirectView):
    url = reverse_lazy('management:create-conversation-template-view')


class FolderCreateView(BSModalCreateView):
    """
    A modal that appears on top of the main_view to create a folder
    """
    template_name = 'template_management/folder_creation_modal.html'
    form_class = FolderCreationForm

    def get_success_url(self):
        success_url = route_to_current_folder(self.request.META.get('HTTP_REFERER'))
        return success_url

    def form_valid(self, form):
        researcher = Researcher.objects.get(pk=self.request.user.id)
        form.instance.researcher = researcher
        return super().form_valid(form)


class FolderEditView(BSModalUpdateView):
    """
    A modal that appears on top of the main_view to edit the contents of a folder
    """
    model = TemplateFolder
    template_name = 'template_management/folder_creation_modal.html'
    form_class = FolderCreationForm

    def get_success_url(self):
        success_url = route_to_current_folder(self.request.META.get('HTTP_REFERER'))
        return success_url


class FolderDeleteView(DeleteView):
    """
    Deletes a folder. Routes to the main_view (all templates showing)
    if the current folder that is being viewed is deleted.
    """
    model = TemplateFolder
    success_url = reverse_lazy('management:main')


class TemplateDeleteView(BSModalDeleteView):
    """
    Deletes a template. Confirmation modal pops up to make sure
    the user wants to delete a template.
    """
    model = ConversationTemplate
    template_name = 'template_management/template_delete_modal.html'
    success_url = reverse_lazy('management:main')

    def get(self, request, *args, **kwargs):
        """
        Override post to send template name and name of assignment that
        will be removed as context to the template
        """
        super().get(request, *args, **kwargs)
        this_template = ConversationTemplate.objects.get(pk=self.kwargs['pk'])
        assignments = this_template.assignments.all()
        to_delete = []
        for assignment in assignments:
            if assignment.conversation_templates.all().count() == 1:
                to_delete.append(assignment.name)
        context = {"template_name": this_template.name, "assignments": to_delete}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Override post to remove assignment if the template being deleted
        is the only one in the assignment.
        """
        this_template = ConversationTemplate.objects.get(pk=self.kwargs['pk'])
        assignments = this_template.assignments.all()
        for assignment in assignments:
            if assignment.conversation_templates.all().count() == 1:
                assignment.delete()
        super().post(request, *args, **kwargs)
        return redirect(reverse('management:main'))


def remove_template(request, pk):
    """
    Remove the chosen template from the current folder in view.
    This does not delete the template.
    """
    if request.method == 'POST':
        previous_url = request.META.get('HTTP_REFERER')
        folder_pk = re.findall(r"/folder/([A-Za-z0-9\-]+)", previous_url)[0]
        template = get_object_or_404(ConversationTemplate, pk=pk)
        folder = get_object_or_404(TemplateFolder, pk=folder_pk)
        folder.templates.remove(template)
        back = request.POST.get('back', '/')
        return redirect(back)


def route_to_current_folder(previous_url):
    """
    If a folder is being viewed returns to the folder view, else to main view
    Used to reroute generic editing views
    """
    if "folder" in previous_url:
        folder_id = re.findall(r"/folder/([A-Za-z0-9\-]+)", previous_url)[0]
        return reverse_lazy('management:folder-view', args=[folder_id])
    else:
        return reverse_lazy('management:main')


def filter_folder(request):
    folder_filter = request.GET.get('folder-filter')
    if folder_filter is not None:
        return TemplateFolder.objects.filter(researcher=request.user.id, name__contains=folder_filter)
    return TemplateFolder.objects.filter(researcher=request.user.id)


def filter_templates(request, templates):
    template_filter = request.GET.get('template-filter')
    if template_filter is not None:
        # Constraint to filter for names OR descriptions that contain the search value
        filter_fields = Q(name__contains=template_filter) | Q(description__contains=template_filter)
        return templates.filter(filter_fields)
    return templates


def get_templates(user):
    researcher = get_object_or_404(Researcher, email=user)
    return ConversationTemplate.objects.filter(researcher=researcher)
