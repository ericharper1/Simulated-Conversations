import django_tables2 as tables


class StudentHomeTable(tables.Table):
    name = tables.Column(linkify={"viewname": "TemplateStartView", "args": [tables.A("conversation_templates__name")]},
                         accessor='conversation_templates__name',
                         verbose_name='Template Name')
    date_assigned = tables.Column(verbose_name='Date Assigned')
    completion_date = tables.Column(accessor='conversation_templates__template_responses__completion_date',
                                    verbose_name='Last Response')
