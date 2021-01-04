from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone
from django.shortcuts import reverse
from http import HTTPStatus
from users.models import Researcher
from .models import TemplateFolder, ConversationTemplate

class TemplateManagementTests(TestCase):
    def setUp(self):
        researcher = Researcher.objects.create_researcher(email="researcher@pdx.edu", password="abc123")
        template1 = ConversationTemplate.objects.create(name="test_template", researcher=researcher,
                                                        creation_date=timezone.now())
        template2 = ConversationTemplate.objects.create(name="another_template", researcher=researcher,
                                                        creation_date=timezone.now())
        folder = TemplateFolder.objects.create(name="folder")
        folder.templates.set([template1, template2])
        self.factory = RequestFactory()

    def test_delete_template(self):
        template_count = ConversationTemplate.objects.count()
        template = ConversationTemplate.objects.get(name="test_template")
        response = self.client.post(reverse('templates:delete_template', args=[template.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ConversationTemplate.objects.count(), template_count - 1)

    def test_create_folder(self):
        template = ConversationTemplate.objects.get(name="test_template")
        folder_count = TemplateFolder.objects.count()
        response = self.client.get(reverse('templates:create_folder'), data={
            "name": "new_folder",
            "templates": template})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response["Location"], '/template-management/')
        self.assertEqual(TemplateFolder.objects.count(), folder_count + 1)

