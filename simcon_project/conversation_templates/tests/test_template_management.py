import time
from django.test import TestCase
from django.utils import timezone
from django.shortcuts import reverse
from http import HTTPStatus
from users.models import Researcher
from ..models import TemplateFolder, ConversationTemplate
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class TemplateManagementTests(TestCase):
    def setUp(self):
        researcher = Researcher.objects.create_researcher(email="researcher@pdx.edu", password="abc123")
        template1 = ConversationTemplate.objects.create(name="test_template", researcher=researcher,
                                                        creation_date=timezone.now())
        template2 = ConversationTemplate.objects.create(name="another_template", researcher=researcher,
                                                        creation_date=timezone.now())
        folder = TemplateFolder.objects.create(name="folder")
        folder.templates.set([template1, template2])

    # =============== UNIT TESTS ===================

    # =============== INTEGRATION TESTS ===================
    def test_create_folder(self):
        template = ConversationTemplate.objects.get(name="test_template")
        folder_count = TemplateFolder.objects.count()
        response = self.client.get(reverse('templates:create_folder'), data={
            "name": "new_folder",
            "templates": template})
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        #self.assertEqual(response["Location"], '/template-management/')
        #self.assertEqual(TemplateFolder.objects.count(), folder_count + 1)

    def test_delete_template(self):
        template_count = ConversationTemplate.objects.count()
        template = ConversationTemplate.objects.get(name="test_template")
        response = self.client.post(reverse('templates:delete_template', args=[template.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ConversationTemplate.objects.count(), template_count - 1)

    # =============== FUNCTIONAL TESTS ===================


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
