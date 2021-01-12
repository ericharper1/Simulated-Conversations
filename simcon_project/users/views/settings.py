from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def SettingsView(request):
    return render(request, 'settings_view.html')
