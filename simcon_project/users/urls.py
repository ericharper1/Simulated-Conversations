from django.urls import path
from .views import *

app_name = 'settings'
urlpatterns = [
    path('', ResearcherSettingsView, name="main"),
    path('delete/<pk>', ResearcherDeleteView.as_view(), name="delete_researcher"),
]
