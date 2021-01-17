from django.urls import path
from .views import *

urlpatterns = [
    path('start/<uuid:ct_id>/', conversation_start, name='conversation_start'),
    path('step/<uuid:ct_node_id>/', conversation_step, name='conversation_step'),
    path('end/<uuid:ct_response_id>/', conversation_end, name='conversation_end'),
]