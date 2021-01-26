from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def StudentUserView(request):
    return render(request, 'studentuser_view.html')