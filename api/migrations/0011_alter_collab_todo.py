
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_collab_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collab',
            name='todo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborations', to='api.todo'),
        ),
    ]
