"""simcon_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from conversation_templates.views import *
from users.views import *
from django.conf.urls import include
from django.contrib.auth import views

urlpatterns = [
    # Redirects and such
    path('', views.LoginView.as_view(), name="Login"),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('redirect-from-login/', RedirectFromLogin, name="RedirectFromLogin"),

    # Todo: remove
    path('user-view/', ResearcherUserView, name="ResearcherUserView"),
    path('studentuser-view/', StudentUserView, name="StudentUserView"),

    # Stuff students can see
    path('student/', StudentView, name="StudentView"),
    path('student/settings/', StudentSettingsView, name="StudentSettingsView"),
    path('student/register/<uidb64>/', UserRegistration, name="UserRegistration"),
    path('student/conversation/', include('conversation_templates.urls.conv_urls'), name='conversation'),

    # Stuff researcher can see
    path('researcher/', ResearcherView, name="ResearcherView"),
    path('researcher/register/<uidb64>/', ResearcherRegistration, name="ResearcherRegistration"),
    path('researcher/templates/', include('conversation_templates.urls.templates_urls'), name="TemplateManagementView"),
    path('researcher/settings/', include('users.urls'), name="ResearcherSettingsView"),
    path('researcher/view-all-responses/<uuid:pk>/', TemplateResponsesView.as_view(), name="ViewAllResponses"),
    path('researcher/students/<str:name>/', StudentManagement, name="StudentManagement"),
    path('researcher/students/', StudentManagement, name="StudentManagement"),
    path('researcher/response/', ViewResponse, name="ViewResponse"),
    path('researcher/response/update/<uuid:pk>/', UpdateOverallResponseFeedback, name='UpdateOverallResponseFeedback'),
    path('researcher/response/updatenode/<uuid:pk>/', UpdateNodeResponseFeedback, name='UpdateNodeResponseFeedback'),
    ]
