# Generated by Django 5.1.3 on 2024-11-28 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0012_alter_practice_practice_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice',
            name='practice_time',
            field=models.TimeField(),
        ),
    ]
