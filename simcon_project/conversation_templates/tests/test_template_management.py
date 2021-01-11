import time
from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.shortcuts import reverse
from users.models import Researcher
from ..models import TemplateFolder, ConversationTemplate
from ..forms import FolderCreationForm
from ..views.template_management import FolderCreateView, remove_template, route_to_current_folder, main_view
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


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
        form = FolderCreationForm({
            'name': "test_folder",
            'templates': [self.template1],
        })
        self.assertTrue(form.is_valid())

    def test_folder_creation_form_invalid_data(self):
        form = FolderCreationForm({
            'name': "",
            'templates': [self.template1],
        })
        self.assertFalse(form.is_valid())

    def test_folder_name_exceeds_max_length(self):
        name = "This is a long string"
        max_len = TemplateFolder._meta.get_field('name').max_length
        for x in range(max_len):
            name = name + 'a'
        form = FolderCreationForm({"name": name, "templates": []})
        expected = [f'Ensure this value has at most {max_len} characters (it has {len(name)}).']
        self.assertEqual(form.errors["name"], expected)

    def test_folder_name_already_exists(self):
        name = "folder"
        form = FolderCreationForm({"name": name, "templates": []})
        expected = [f'Folder named {name} already exists.']
        self.assertEqual(form.errors["name"], expected)

    def test_route_to_existing_url_with_folder(self):
        request = self.factory.get(reverse('templates:folder_view', args=[self.folder.id]))
        response = route_to_current_folder(request.get_full_path())
        self.assertEqual(response, reverse('templates:folder_view', args=[self.folder.id]))

    def test_route_to_existing_url_no_folder(self):
        request = self.factory.get(reverse('templates:main'))
        response = route_to_current_folder(request.get_full_path())
        self.assertEqual(response, reverse('templates:main'))

    def test_main_view_displaying_all_templates(self):
        response = self.client.post(reverse('templates:main'))
        self.assertIn('AllTemplateTable', str(type(response.context['templateTable'])))

    def test_main_view_displaying_folder_content(self):
        request = self.factory.get(reverse('templates:main'))
        request.get(reverse('templates:folder_view', args=[self.folder.id]))
        self.assertEqual(self.factory.request(), '')
        self.assertEqual(request.META.get('HTTP_REFERER'), '')
        response = self.client.post(reverse('templates:folder_view', args=[self.folder.id]))
        self.assertIn('AllTemplateTable', str(type(response.context['templateTable'])))

    # =============== INTEGRATION TESTS ===================
    #def test_create_folder2(self):
    #    folder_count = TemplateFolder.objects.count()
    #    data = {"name": "new_folder", 'templates': self.template1}
    #    request = self.factory.post(reverse('templates:create_folder'), data=data)
    #    view = FolderCreateView()
    #    view.setup(request)
    #    self.assertEqual(TemplateFolder.objects.count(), folder_count + 1)

    #def test_create_folder(self):
        #folder_count = TemplateFolder.objects.count()
        #response = self.client.post(reverse('templates:create_folder'), data={
        #    "name": "new_folder",
        #    "templates": self.template1})
        #self.assertEqual(response, '')
        #self.assertEqual(response.status_code, 200)
        #self.assertEqual(TemplateFolder.objects.count(), folder_count + 1)

    #def test_remove_template(self):
    #    pre_template_count = self.folder.templates.count()
    #    self.factory.get(reverse('templates:folder_view', args=[self.folder.id]))
    #    self.factory.post(reverse('templates:remove_template', args=[self.template1.id]))
    #    post_template_count = self.folder.templates.count()
    #    self.assertEqual(post_template_count, pre_template_count - 1)

    def test_delete_template(self):
        template_count = ConversationTemplate.objects.count()
        response = self.client.post(reverse('templates:delete_template', args=[self.template1.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ConversationTemplate.objects.count(), template_count - 1)

    def test_delete_folder(self):
        folder_count = TemplateFolder.objects.count()
        response = self.client.post(reverse('templates:delete_folder', args=[self.folder.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TemplateFolder.objects.count(), folder_count - 1)
    # =============== FUNCTIONAL TESTS ===================


"""
class SeleniumTest(LiveServerTestCase):
    @classmethod
    def setUpClass(self):
        super().setUpClass()
        self.selenium = WebDriver('chromedriver.exe')
        self.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        researcher = Researcher.objects.create_researcher(email="researcher@pdx.edu", password="abc123")
        template1 = ConversationTemplate.objects.create(name="test_template", researcher=researcher,
                                                        creation_date=timezone.now())
        template2 = ConversationTemplate.objects.create(name="another_template", researcher=researcher,
                                                        creation_date=timezone.now())
        folder = TemplateFolder.objects.create(name="folder")
        folder.templates.set([template1, template2])

    def test_delete_template(self):
        self.selenium.get('%s%s' % (self.live_server_url, reverse('templates:main')))
        time.sleep(2)
        delete_template_button = self.selenium.find_element_by_name("delete_folder_btn")
        delete_template_button.click()
        time.sleep(3)

    #def test_blah(self):
    #    self.selenium.get('%s%s' % (self.live_server_url, reverse('templates:main')))
    #    create_folder_button = self.selenium.find_element_by_name("create_folder_btn")
    #    create_folder_button.click()
    #    modal = self.selenium.find_elements_by_xpath(".//div[@class='modal-footer']")
    #    folder_name = self.selenium.find_element_by_name("name")
    #    folder_name.send_keys('myuser')
    #    WebDriverWait(self.selenium, 10).until(expect.element_to_be_clickable
    #                                           ((By.XPATH, "//button[@class='btn btn-success']")))
    #    self.selenium.find_element(By.XPATH, "//button[@class='btn btn-success']").click()
    #    #save_button = self.selenium.find_element_by_class_name("btn-success")
    #    #save_button.click()
    #    time.sleep(1)
"""
