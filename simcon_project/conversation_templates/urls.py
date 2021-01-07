from django.urls import path
from .views import *

app_name = 'templates'
urlpatterns = [
    path('', TemplateManagementView.as_view(), name="main"),
    path('<uuid:pk>', TemplateManagementView.as_view(), name="template_management"),
    path('folder/create', create_folder, name="create_folder"),
    path('folder/delete/<uuid:pk>', delete_folder, name="delete_folder"),
    path('folder/edit/<uuid:pk>', edit_folder, name="edit_folder"),
    path('template/delete/<uuid:pk>', delete_template, name="delete_template"),
    path('folder/<uuid:folder_pk>/remove/<uuid:template_pk>', remove_template, name="remove_template"),
    path('folder/creation_menu', FolderCreateView.as_view(), name='create_modal'),
    path('folder/update_menu', FolderCreateView.as_view(), name='update_modal'),
]