# Generated by Django 3.1.3 on 2021-01-01 07:41

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConversationTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=4000)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='TemplateNode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('description', models.CharField(max_length=4000)),
                ('video_url', models.URLField(max_length=100)),
                ('start', models.BooleanField(default=False)),
                ('terminal', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TemplateNodeChoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('choice_text', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='TemplateNodeResponse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('transcription', models.CharField(max_length=1000)),
                ('position_in_sequence', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TemplateResponse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('completion_date', models.DateTimeField(default=None)),
            ],
        ),
    ]
