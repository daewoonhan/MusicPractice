# Generated by Django 5.1.3 on 2024-11-28 06:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_alter_token_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 5, 6, 30, 38, 87380, tzinfo=datetime.timezone.utc)),
        ),
    ]
