# Generated by Django 3.0.7 on 2021-08-07 16:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_todo_collaborator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='collaborator',
            field=models.ManyToManyField(related_name='collaborator', to=settings.AUTH_USER_MODEL),
        ),
    ]
