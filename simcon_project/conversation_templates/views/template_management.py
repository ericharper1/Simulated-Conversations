from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from conversation_templates.models import ConversationTemplate, TemplateFolder
from conversation_templates.forms import FolderCreationForm
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
    name = tables.columns.LinkColumn('management:folder_view', args=[A('pk')])

    class Meta:
        attrs = {'class': 'table table-sm', 'id': 'template-table'}
        model = ConversationTemplate
        fields = ['name', 'description', 'creation_date']


class FolderTable(tables.Table):
    """
    Table showing all folders (unique to a researcher in the future)
    """
    name = tables.columns.LinkColumn('management:folder_view', args=[A('pk')])

    class Meta:
        attrs = {'class': 'table table-sm', 'id': 'folder-table'}
        model = TemplateFolder
        fields = ['name']


def main_view(request):
    """
    Main template management view.
    Main contents of the page are the tables showing all templates and folders the researcher has created.
    """
    templates = ConversationTemplate.objects.all()
    template_table = AllTemplateTable(templates)

    folders = TemplateFolder.objects.all()
    folder_table = FolderTable(folders)

    RequestConfig(request, paginate=False).configure(template_table)
    RequestConfig(request, paginate=False).configure(folder_table)

    context = {
        'templateTable': template_table,
        'folderTable': folder_table,
        'folder_pk': None,
    }

    return render(request, 'template_management/main_view.html', context)


def folder_view(request, pk):
    """
    Main template management view.
    Shows the all folders, but shows only templates belonging to the selected folder
    """
    current_folder = get_object_or_404(TemplateFolder, pk=pk)
    templates = current_folder.templates.all()
    template_table = FolderTemplateTable(templates)

    folders = TemplateFolder.objects.all()
    folder_table = FolderTable(folders)

    RequestConfig(request, paginate=False).configure(template_table)
    RequestConfig(request, paginate=False).configure(folder_table)

    context = {
        'templateTable': template_table,
        'folderTable': folder_table,
        'folder_pk': pk
    }

    return render(request, 'template_management/main_view.html', context)


class FolderCreateView(BSModalCreateView):
    """
    A modal that appears on top of the main_view to create a folder
    """
    template_name = 'template_management/folder_creation_modal.html'
    form_class = FolderCreationForm
    success_message = 'Success: Folder was created.'

    def get_success_url(self):
        success_url = route_to_current_folder(self.request.META.get('HTTP_REFERER'))
        return success_url


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
    success_message = 'Success: Book was deleted.'
    success_url = reverse_lazy('management:main')


class TemplateDeleteView(BSModalDeleteView):
    """
    Deletes a template. Confirmation modal pops up to make sure
    the user wants to delete a template.
    """
    model = ConversationTemplate
    template_name = 'template_management/template_delete_modal.html'
    success_message = 'Success: Book was deleted.'
    success_url = reverse_lazy('management:main')


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
        return reverse_lazy('management:folder_view', args=[folder_id])
    else:
        return reverse_lazy('management:main')
