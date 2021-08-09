# Generated by Django 3.2.6 on 2021-08-05 11:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0004_auto_20210805_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='collab',
            field=models.ManyToManyField(related_name='collab', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Collab',
        ),
    ]
