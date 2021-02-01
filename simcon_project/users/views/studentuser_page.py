from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from users.views.student_home import is_student


@user_passes_test(is_student)
def student_user_view(request):
    return render(request, 'studentuser_view.html')
