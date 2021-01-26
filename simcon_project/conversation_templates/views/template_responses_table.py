from django.shortcuts import render
from django_tables2 import tables, RequestConfig, SingleTableView
from django_tables2.export.views import TableExport
from conversation_templates.models import ConversationTemplate, TemplateFolder, TemplateResponse


class ResponseTable(tables.Table):
    first = tables.columns.Column()
    last = tables.columns.Column()

    class Meta:
        model = TemplateResponse
        fields = ['first', 'last', 'completion_date']


class TemplateResponsesView(SingleTableView):
    model = TemplateResponse
    table_class = ResponseTable
    template_name = "template_all_response_view.html"

    def get(self, request, pk):
        template = ConversationTemplate.objects.get(pk=pk)
        descriptions = []  # Description of template node used for column header
        extra_columns = []  # List of tuples of description and column object to pass to table
        table_data = []  # List of dictionaries to populate table. 1 dictionary = 1 column

        for node in template.template_nodes.all():
            descriptions.append(node.description)
            extra_columns.append((node.description, tables.columns.Column()))

        for response in template.template_responses.all().order_by('-completion_date'):
            column_data = {
                "first": response.student.first_name,
                "last": response.student.last_name,
                "completion_date": response.completion_date,
            }

            for idx, node in enumerate(response.node_responses.all()):
                column_data.update({descriptions[idx]: node.transcription})

            table_data.append(column_data)

        response_table = ResponseTable(data=table_data, extra_columns=extra_columns)
        RequestConfig(request, paginate=False).configure(response_table)
        export_format = request.GET.get("_export", None)
        context = {
            "table": response_table,
        }

        if TableExport.is_valid_format(export_format):
            exporter = TableExport(export_format, response_table)
            file_name = f"{template.name}.{format(export_format)}"
            return exporter.response(file_name)

        return render(request, self.template_name, context)
