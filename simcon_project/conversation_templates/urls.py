from django.urls import path
from .views import *

app_name = 'templates'
urlpatterns = [
    path('', TemplateManagementView.as_view(), name="template_management"),
    path('create/', FolderCreateView.as_view(), name="create_folder"),
    path('folder/delete/<uuid:pk>', delete_folder, name="delete_folder"),
    path('template/delete/<uuid:pk>', delete_template, name="delete_template"),
]