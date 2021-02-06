from django.urls import path
from users.views import *

app_name = 'ass-management'
urlpatterns = [
    path('', assignment_management_view, name="main"),
    path('view/<pk>/', view_templates, name="view-templates"),
    path('delete/<pk>', AssignmentDeleteView.as_view(), name="delete-assignment"),
]
