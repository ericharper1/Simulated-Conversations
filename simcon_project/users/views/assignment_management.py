import django_tables2 as tables
from django_tables2.config import RequestConfig
from django.contrib.auth.decorators import user_passes_test
from users.views.researcher_home import is_researcher
from users.models import Assignment


class AssignmentsTable(tables.table):
    name = tables.Column()
    date_assigned = tables.Column()
    templates = tables.TemplateColumn() # modal to see contained templates. They link to template_management
    completion = tables.Column() # maybe percentage and actual counts
    delete = tables.TemplateColumn()



@user_passes_test(is_researcher)
def assignment_management(request):
    researcher = 