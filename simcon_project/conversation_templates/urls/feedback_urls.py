from django.urls import path
from conversation_templates.views import view_response
from users.views.student_home import select_feedback_view

app_name = 'feedback'
urlpatterns = [
    path('select/<pk_assignment>/<pk_template>/', select_feedback_view, name="select-feedback"),
    path('view/<pk>/', view_response, name="view-feedback"),
]