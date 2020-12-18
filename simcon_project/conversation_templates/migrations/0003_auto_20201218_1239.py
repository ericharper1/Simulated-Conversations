# Generated by Django 3.1.3 on 2020-12-18 20:39

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20201214_1716'),
        ('conversation_templates', '0002_auto_20201214_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversationtemplate',
            name='nodes',
        ),
        migrations.RemoveField(
            model_name='templatenode',
            name='choices',
        ),
        migrations.RemoveField(
            model_name='templatenodechoice',
            name='node_id',
        ),
        migrations.AddField(
            model_name='conversationtemplate',
            name='researcher',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='templates', to='users.researcher'),
        ),
        migrations.AddField(
            model_name='templatenode',
            name='parent_template',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='template_nodes', to='conversation_templates.conversationtemplate'),
        ),
        migrations.AddField(
            model_name='templatenodechoice',
            name='destination_node',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent_choices', to='conversation_templates.templatenode'),
        ),
        migrations.AddField(
            model_name='templatenodechoice',
            name='parent_template',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='choices', to='conversation_templates.templatenode'),
        ),
        migrations.AddField(
            model_name='templatenoderesponse',
            name='parent_template_response',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='node_responses', to='conversation_templates.templateresponse'),
        ),
        migrations.AddField(
            model_name='templateresponse',
            name='assignment',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='template_responses', to='users.assignment'),
        ),
        migrations.AddField(
            model_name='templateresponse',
            name='student',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='template_responses', to='users.student'),
        ),
        migrations.AlterField(
            model_name='conversationtemplate',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='templatenode',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='templatenode',
            name='video_url',
            field=models.URLField(max_length=100),
        ),
        migrations.AlterField(
            model_name='templatenodechoice',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='templatenoderesponse',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.RemoveField(
            model_name='templatenoderesponse',
            name='template_node',
        ),
        migrations.AddField(
            model_name='templatenoderesponse',
            name='template_node',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='responses', to='conversation_templates.templatenode'),
        ),
        migrations.AlterField(
            model_name='templateresponse',
            name='completion_date',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='templateresponse',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='templateresponse',
            name='template',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='template_responses', to='conversation_templates.conversationtemplate'),
        ),
    ]
