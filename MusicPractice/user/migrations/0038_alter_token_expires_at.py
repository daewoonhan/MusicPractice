# Generated by Django 5.1.3 on 2024-11-28 14:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0037_alter_token_expires_at_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 5, 14, 48, 59, 712442, tzinfo=datetime.timezone.utc)),
        ),
    ]