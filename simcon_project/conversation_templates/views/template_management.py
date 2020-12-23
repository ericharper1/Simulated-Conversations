from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from conversation_templates.models import ConversationTemplate, TemplateFolder
from conversation_templates.forms import FolderCreationForm


class FolderCreateView(BSModalCreateView):
    template_name = 'folder_creation_modal.html'
    form_class = FolderCreationForm
    success_message = 'Success: New Folder was created.'
    success_url = '/'


class TemplateManagementView(TemplateView):
    context = {
        "templates": ConversationTemplate.objects.all(),
        "folders": TemplateFolder.objects.all(),
    }

    def get(self, request):
        form = FolderCreationForm()
        self.context.update({"form": form})
        return render(request, 'template_management.html', self.context)

    def post(self, request):
        form = FolderCreationForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['name']
            folder = TemplateFolder.objects.create_folder(text)
            folder.save()
            return redirect('/template-management')

        form = FolderCreationForm()
        self.context.update({"form": form})
        return render(request, 'template_management.html', self.context)


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


def create_template(request, pk):
    """
        Just route to template creation page
    """
    return render(request, 'template_management.html')
