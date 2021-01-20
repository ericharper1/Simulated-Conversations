from django.urls import path
from .views import *

app_name = 'management'
urlpatterns = [
    path('', MainView, name="main"),
    path('folder/<uuid:pk>', FolderView, name="folder_view"),
    path('folder/create', FolderCreateView.as_view(), name='create_folder'),
    path('folder/delete/<uuid:pk>', FolderDeleteView.as_view(), name='delete_folder'),
    path('folder/edit/<uuid:pk>', FolderEditView.as_view(), name='edit_folder'),
    path('templates/delete/<uuid:pk>', TemplateDeleteView.as_view(), name="delete_template"),
    path('folder/remove/<uuid:pk>', RemoveTemplate, name="remove_template"),
]
