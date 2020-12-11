from django.contrib.auth import get_user_model
from users.models.custom_user import CustomUser
from .researcher_home import ResearcherView
from .student_home import StudentView

def RedirectFromLogin(request):
    user = get_user_model()
    if user.get_is_researcher(request.user) == True:
        return ResearcherView(request)
    else:
        return StudentView(request)