from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def StudentSettingsView(request):
    return render(request, 'student_settings_view.html')
