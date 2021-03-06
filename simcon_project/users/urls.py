from django.urls import path
from .views import *

app_name = 'settings'
urlpatterns = [
    path('', researcher_settings_view, name="main"),
    path('delete/<pk>/', ResearcherDeleteView.as_view(), name="delete-researcher"),
]
