from django.urls import path
from conversation_templates.views import *

app_name = 'management'
urlpatterns = [
    path('', main_view, name="main"),
    path('folder/<uuid:pk>/', folder_view, name="folder_view"),
    path('folder/new/', FolderCreateView.as_view(), name='create_folder'),
    path('folder/delete/<uuid:pk>/',
         FolderDeleteView.as_view(), name='delete_folder'),
    path('folder/edit/<uuid:pk>/', FolderEditView.as_view(), name='edit_folder'),
    path('templates/delete/<uuid:pk>/',
         TemplateDeleteView.as_view(), name="delete_template"),
    path('folder/remove/<uuid:pk>/', remove_template, name="remove_template"),
]
