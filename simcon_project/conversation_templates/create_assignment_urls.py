from django.urls import path
from .views import *

app_name = 'assignments'
urlpatterns = [
    path('', CreateAssignmentView.as_view(), name="create_assignment"),
    path('add_data/', add_data, name="add_data"),
]