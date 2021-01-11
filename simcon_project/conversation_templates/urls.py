from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^start/(?P<ct_id>[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12})/$',
        views.conversation_start, name='conversation_start'),
    url(r'^step/(?P<ctn_id>[0-9a-fA-F]{8}-?[0-9a-fA-F]{4}-?4[0-9a-fA-F]{3}-?[89abAB][0-9a-fA-F]{3}-?[0-9a-fA-F]{12})/$',
        views.conversation_step, name='conversation_step'),
    url(r'^end/', views.conversation_end, name='conversation_end'),
]