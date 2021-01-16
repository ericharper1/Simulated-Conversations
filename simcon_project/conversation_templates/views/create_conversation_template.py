from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_researcher(user):
    return user.is_authenticated and user.is_researcher

@user_passes_test(is_researcher)
def CreateConversationTemplateView(request):
    return render(request, 'conversation_templates/create_conversation_template.html')