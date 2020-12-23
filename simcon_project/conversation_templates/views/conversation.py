from django.template import loader, RequestContext, Context
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model

# Globals
ct_templates_dir = 'conversation'
user = get_user_model()


# Returns data for Request process
def proc_metadata(request):
    return {
        'user_email': request.user.__str__(),
    }


# Views
def conversation_start(request):
    ctx = proc_metadata(request)
    ctx_params = {}
    ctx.update(ctx_params)
    t = loader.get_template('{}/conversation_start.html'.format(ct_templates_dir))
    return HttpResponse(t.render(ctx))


def conversation_step(request):
    ctx = proc_metadata(request)
    ctx_params = {}
    ctx.update(ctx_params)
    t = loader.get_template('{}/conversation_step.html'.format(ct_templates_dir))
    return HttpResponse(t.render(ctx))


def conversation_end(request):
    ctx = proc_metadata(request)
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

    ctx_params = {'ct_list': ct_list}
    ctx.update(ctx_params)
    t = loader.get_template('{}/conversation_end.html'.format(ct_templates_dir))
    return HttpResponse(t.render(ctx))
