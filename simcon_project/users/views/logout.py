from django.contrib.auth import logout as auth_logout
from django.shortcuts import render


def logout(request):
    return auth_logout(request)
