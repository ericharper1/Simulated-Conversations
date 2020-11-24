from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser
from django.template import loader, Context

# Create your views here.
def Login(request):

    t = loader.get_template('Login.html')
    c = Context({
    'message': 'I am the Login View.'
    })
    request.session.modified = True
    return render(request, 'Login.html')