from django.shortcuts import render
from django.contrib.auth import get_user_model
from users.models import *
from conversation_templates.models import *


def StudentView(request):
    assigned_templates = Assignment.objects.filter(students=request.user.id)\
        .values_list(
            'conversation_templates__name',
            'date_assigned',
            'conversation_templates__template_responses__completion_date')\
        .order_by('conversation_templates__template_responses__completion_date', 'date_assigned')
    # must pass context as a dictionary
    table_dict = {
        'assigned_templates': assigned_templates
    }
    return render(request, 'student_view.html', table_dict)
