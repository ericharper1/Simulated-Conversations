from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse

# Create your views here.
ct_templates_dir = 'conversation'
def conversation_start(request):
    ctx = {}
    t_name = '{}/conversation_start.html'.format(ct_templates_dir)
    t = get_template(t_name)
    html = t.render(ctx)
    return HttpResponse(html)

def conversation_step(request):
    ctx = {}
    t_name = '{}/conversation_step.html'.format(ct_templates_dir)
    t = get_template(t_name)
    html = t.render(ctx)
    return HttpResponse(html)

def conversation_end(request):
    # for testing
    ct_list = [
        {
            'description': 'scene1',
            'transcription': 'response1'
        },
        {
            'description': 'scene2',
            'transcription': 'response2'
        },
        {
            'description': 'scene3',
            'transcription': 'response3'
        }
    ]

    ctx = {'ct_list': ct_list}
    t_name = '{}/conversation_end.html'.format(ct_templates_dir)
    t = get_template(t_name)
    html = t.render(ctx)
    return HttpResponse(html)
