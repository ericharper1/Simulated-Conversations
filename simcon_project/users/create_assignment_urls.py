from django.urls import path
from users.views import *

app_name = 'assignments'
urlpatterns = [
    path('', CreateAssignmentView.as_view(), name="create-assignment"),
    path('add_data/', add_data, name="add-data"),
]
