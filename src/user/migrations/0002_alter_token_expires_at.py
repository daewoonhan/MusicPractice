# Generated by Django 5.1.3 on 2024-11-26 16:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 3, 16, 37, 33, 811559, tzinfo=datetime.timezone.utc)),
        ),
    ]
