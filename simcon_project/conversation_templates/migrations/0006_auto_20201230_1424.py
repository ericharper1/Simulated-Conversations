# Generated by Django 3.1.3 on 2020-12-30 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversation_templates', '0005_auto_20201221_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templatefolder',
            name='templates',
            field=models.ManyToManyField(blank=True, default=None, related_name='folder', to='conversation_templates.ConversationTemplate'),
        ),
    ]
