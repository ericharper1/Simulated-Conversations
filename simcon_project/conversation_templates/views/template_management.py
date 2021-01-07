from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from conversation_templates.models import ConversationTemplate, TemplateFolder
from conversation_templates.forms import FolderCreationForm
from bootstrap_modal_forms.generic import BSModalCreateView, BSModalUpdateView


class FolderCreateView(BSModalCreateView):
    template_name = 'folder_creation_modal.html'
    form_class = FolderCreationForm
    success_message = 'Success: Folder was created.'
    success_url = reverse_lazy('templates:main')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        templates = form['templates'].value()
        folder = TemplateFolder.objects.create_folder(name)
        folder.templates.set(templates)
        folder.save()
        return redirect(reverse('templates:main'))


class FolderUpdateView(BSModalUpdateView):
    template_name = 'folder_creation_modal.html'
    form_class = FolderCreationForm
    success_message = 'Success: Folder was created.'
    success_url = reverse_lazy('templates:main')


class TemplateManagementView(TemplateView):
    context = {
        "templates": ConversationTemplate.objects.all(),
        "folders": TemplateFolder.objects.all(),
        "current_folder": None,
        "form": FolderCreationForm(),
    }

    def get(self, request, pk=None):
        """
        Reset the context to default (no folder selected, all templates showing)
        if redirected from static views or if the current_folder is not in the
        current path (redirected from post method in this class)
        """
        current_folder = self.context["current_folder"]
        if current_folder is None or str(current_folder) not in request.path:
            self.context.update({
               "templates": ConversationTemplate.objects.all(),
               "form": FolderCreationForm(),
               "folders": TemplateFolder.objects.all(),
               "current_folder": None,
            })
        return render(request, 'template_management/main_view.html', self.context)

    def post(self, request, pk):
        folder = get_object_or_404(TemplateFolder, pk=pk)
        # Display content of folder if it was not currently selected/displayed
        # If current folder is selected again return to main view
        if self.context["current_folder"] != pk:
            form_fields = {"name": folder.name, "templates": folder.templates.all()}
            form = FolderCreationForm(initial=form_fields)
            templates = folder.templates.all()
            self.context.update({"templates": templates, "current_folder": pk, "form": form})
            print(folder.name)
            print(templates)
            return render(request, 'template_management/main_view.html', self.context)
        else:
            return redirect("/template-management")


def create_folder(request):
    """
    Uses empty_form from context to give user a blank form to create a TemplateFolder object
    """
    form = FolderCreationForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data['name']
            templates = form['templates'].value()
            folder = TemplateFolder.objects.create_folder(name)
            folder.templates.set(templates)
            folder.save()
        return redirect('/template-management')


def create_template(request, pk):
    """
    Route to template creation page
    """


def delete_folder(request, pk):
    folder = get_object_or_404(TemplateFolder, pk=pk)

    if request.method == 'POST':
        folder.delete()

    return redirect('/template-management')


def delete_template(request, pk):
    template = get_object_or_404(ConversationTemplate, pk=pk)

    if request.method == 'POST':
        template.delete()

    return redirect('/template-management')


def edit_folder(request, pk):
    """
    Populate FolderCreationForm with the current_folder's data to let the user
    edit the name and templates associated to that folder.
    This option is only shown when a folder is selected.
    """
    folder = get_object_or_404(TemplateFolder, pk=pk)
    form_fields = {"name": folder.name, "templates": folder.templates.all()}
    form = FolderCreationForm(request.POST, initial=form_fields)
    if form.is_valid():
        name = form.cleaned_data['name']
        templates = form['templates'].value()
        TemplateFolder.objects.filter(pk=pk).update(name=name)
        folder.templates.set(templates)
        return redirect(reverse('templates:template_management', args=[folder.id]))

    return redirect(reverse("templates:main"))


def remove_template(request, template_pk, folder_pk):
    """
    Remove the chosen template from the current_folder.
    This does not delete the template.
    """
    template = get_object_or_404(ConversationTemplate, pk=template_pk)
    folder = get_object_or_404(TemplateFolder, pk=folder_pk)

    if request.method == 'POST':
        folder.templates.remove(template)

    return redirect(reverse('templates:template_management', args=[folder.id]))
