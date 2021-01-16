from django.shortcuts import render

def StudentView(request):
    return render(request, 'student_view.html')