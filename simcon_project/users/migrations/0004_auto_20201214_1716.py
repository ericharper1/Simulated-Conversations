# Generated by Django 3.1.3 on 2020-12-15 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conversation_templates', '0001_initial'),
        ('users', '0003_auto_20201130_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('date_assigned', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.customuser')),
                ('registered', models.BooleanField(default=False)),
                ('available_templates', models.ManyToManyField(related_name='students_incomplete', to='conversation_templates.ConversationTemplate')),
                ('completed_templates', models.ManyToManyField(related_name='student_complete', to='conversation_templates.ConversationTemplate')),
                ('template_response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conversation_templates.templateresponse')),
            ],
            options={
                'abstract': False,
            },
            bases=('users.customuser',),
        ),
        migrations.CreateModel(
            name='SubjectLabel',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('file_name', models.CharField(max_length=100)),
                ('students', models.ManyToManyField(related_name='subject_labels', to='users.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('customuser_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='users.customuser')),
                ('assignments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.assignment')),
                ('labels', models.ManyToManyField(related_name='researchers', to='users.SubjectLabel')),
                ('students', models.ManyToManyField(related_name='researchers', to='users.Student')),
                ('templates', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conversation_templates.conversationtemplate')),
            ],
            options={
                'abstract': False,
            },
            bases=('users.customuser',),
        ),
        migrations.AddField(
            model_name='assignment',
            name='labels',
            field=models.ManyToManyField(related_name='assignments', to='users.SubjectLabel'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='students',
            field=models.ManyToManyField(related_name='assignments', to='users.Student'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='templates',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='conversation_templates.conversationtemplate'),
        ),
    ]
