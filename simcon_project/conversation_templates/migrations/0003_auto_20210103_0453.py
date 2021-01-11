# Generated by Django 3.1.3 on 2021-01-03 04:53

from django.db import migrations, models
import django.db.models.deletion
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('conversation_templates', '0002_auto_20210101_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templatenode',
            name='video_url',
            field=embed_video.fields.EmbedVideoField(),
        ),
        migrations.AlterField(
            model_name='templatenodechoice',
            name='destination_node',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent_choices', to='conversation_templates.templatenode'),
        ),
    ]
