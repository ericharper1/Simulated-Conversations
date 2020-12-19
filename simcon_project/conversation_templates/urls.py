from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^start/', views.conversation_start, name='conversation_start'),
    url(r'^step/', views.conversation_step, name='conversation_step'),
    url(r'^end/', views.conversation_end, name='conversation_end'),
]