from django.shortcuts import render

def StudentView(request):
    return render(request, 'users/student_view.html')