# Generated by Django 5.1.3 on 2024-11-26 18:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_remove_user_username_alter_token_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 3, 18, 26, 45, 744925, tzinfo=datetime.timezone.utc)),
        ),
    ]
