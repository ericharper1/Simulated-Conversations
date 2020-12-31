from django.shortcuts import render


def SettingsView(request):
    return render(request, 'settings_view.html')