# Generated by Django 5.1.3 on 2024-11-26 19:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_alter_token_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 3, 19, 49, 39, 386319, tzinfo=datetime.timezone.utc)),
        ),
    ]
