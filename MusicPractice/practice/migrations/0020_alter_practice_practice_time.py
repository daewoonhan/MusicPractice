# Generated by Django 5.1.3 on 2024-11-28 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0019_practice_practice_count_practice_practice_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice',
            name='practice_time',
            field=models.TimeField(),
        ),
    ]
