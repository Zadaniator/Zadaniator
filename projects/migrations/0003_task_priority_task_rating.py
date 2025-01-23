# Generated by Django 5.1.5 on 2025-01-23 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_updated_at_task_created_at_task_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='task',
            name='rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]