from django.shortcuts import render

def ViewResponse(request):
    return render(request, 'view_response.html')