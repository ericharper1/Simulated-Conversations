from django.test import TestCase
from django.test.client import RequestFactory
from django.apps import apps
from django.utils import timezone
from django.shortcuts import reverse
from .models import TemplateFolder, ConversationTemplate
from .views import TemplateManagementView

class TemplateManagementTests(TestCase):
    def setUp(self):
        template1 = ConversationTemplate.objects.create(name="test_template",
                                                        creation_date=timezone.now())
        template2 = ConversationTemplate.objects.create(name="another_template",
                                                        creation_date=timezone.now())
        folder = TemplateFolder.objects.create(name="folder", templates=[template1, template2])
        self.factory = RequestFactory()

    def test_delete_template(self):
        template = ConversationTemplate.objects.get(name="test_template")
        response = self.factory.post(reverse('templates:delete_template', args=[template.id]))
        self.assertEqual(response.status_code, 200)
