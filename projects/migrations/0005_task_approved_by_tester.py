# Generated by Django 5.1.5 on 2025-01-24 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_remove_task_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='approved_by_tester',
            field=models.BooleanField(default=False),
        ),
    ]