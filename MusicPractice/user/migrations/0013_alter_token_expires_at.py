# Generated by Django 5.1.3 on 2024-11-27 01:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0012_alter_token_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 4, 1, 49, 51, 801757, tzinfo=datetime.timezone.utc)),
        ),
    ]
