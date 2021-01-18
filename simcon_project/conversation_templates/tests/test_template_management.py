from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.shortcuts import reverse
from users.models import Researcher
from ..models import TemplateFolder, ConversationTemplate
from ..forms import FolderCreationForm
from ..views.template_management import route_to_current_folder, remove_template, FolderEditView


class TemplateManagementTests(TestCase):
    def setUp(self):
        self.researcher = Researcher.objects.create_researcher(email="researcher@pdx.edu", password="abc123")
        self.template1 = ConversationTemplate.objects.create(name="test_template", researcher=self.researcher,
                                                             creation_date=timezone.now())
        self.template2 = ConversationTemplate.objects.create(name="another_template", researcher=self.researcher,
                                                             creation_date=timezone.now())
        self.folder = TemplateFolder.objects.create(name="folder")
        self.folder.templates.set([self.template1, self.template2])
        self.factory = RequestFactory()

    # =============== UNIT TESTS ===================
    def test_folder_creation_form_valid_data(self):
        form = FolderCreationForm(data={'name': "test_folder", 'templates': [self.template1]})
        self.assertTrue(form.is_valid())

    def test_folder_creation_form_invalid_data(self):
        form = FolderCreationForm(data={'name': "", 'templates': [self.template1]})
        self.assertFalse(form.is_valid())

    def test_folder_name_exceeds_max_length(self):
        name = "This is a long string"
        max_len = TemplateFolder._meta.get_field('name').max_length
        for x in range(max_len):
            name = name + 'a'
        form = FolderCreationForm(data={"name": name, "templates": []})
        expected = [f'Ensure this value has at most {max_len} characters (it has {len(name)}).']
        self.assertEqual(form.errors["name"], expected)

    def test_folder_name_already_exists(self):
        name = "folder"
        form = FolderCreationForm(data={"name": name, "templates": []})
        expected = ['Template folder with this Name already exists.']
        self.assertEqual(form.errors["name"], expected)

    def test_route_to_existing_url_with_folder(self):
        request = self.factory.get(reverse('management:folder_view', args=[self.folder.id]))
        response = route_to_current_folder(request.get_full_path())
        self.assertEqual(response, reverse('management:folder_view', args=[self.folder.id]))

    def test_route_to_existing_url_no_folder(self):
        request = self.factory.get(reverse('management:main'))
        response = route_to_current_folder(request.get_full_path())
        self.assertEqual(response, reverse('management:main'))

    def test_main_view(self):
        response = self.client.get(reverse('management:main'))
        self.assertIn('AllTemplateTable', str(type(response.context['templateTable'])))
        self.assertEqual(response.status_code, 200)

    def test_folder_view(self):
        response = self.client.get(reverse('management:folder_view', args=[self.folder.id]))
        self.assertIn('FolderTemplateTable', str(type(response.context['templateTable'])))
        self.assertEqual(response.context['folder_pk'], self.folder.id)
        self.assertEqual(response.status_code, 200)

    def test_edit_folder(self):
        data = {"name": "changed_folder", "templates": []}
        prev_request = self.factory.get(reverse('management:main'))
        request = self.factory.post(reverse('management:edit_folder', args=[self.folder.id]), data=data)
        request.META['HTTP_REFERER'] = prev_request
        response = FolderEditView.as_view()(request, pk=self.folder.id)
        self.assertEqual(response.status_code, 302)

    def test_create_folder(self):
        response = self.client.post(reverse('management:create_folder'), data={
            "name": "new_folder",
            "templates": self.template1})
        self.assertEqual(response.status_code, 200)

    def test_delete_template(self):
        template_count = ConversationTemplate.objects.count()
        response = self.client.post(reverse('management:delete_template', args=[self.template1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ConversationTemplate.objects.count(), template_count - 1)

    def test_delete_folder(self):
        folder_count = TemplateFolder.objects.count()
        response = self.client.post(reverse('management:delete_folder', args=[self.folder.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TemplateFolder.objects.count(), folder_count - 1)
