from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

# Create your views here.
def conversation_start(request):
    context = {}
    t = get_template('conversation/conversation_start.html')
    html = t.render(Context(context))
    return HttpResponse(html)

def conversation_step(request):
    context = {}
    t = get_template('conversation/conversation_step.html')
    html = t.render(Context(context))
    return HttpResponse(html)

def conversation_end(request):
    context = {}
    t = get_template('conversation/conversation_end.html')
    html = t.render(Context(context))
    return HttpResponse(html)
