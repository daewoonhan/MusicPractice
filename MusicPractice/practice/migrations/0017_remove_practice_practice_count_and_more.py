# Generated by Django 5.1.3 on 2024-11-28 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0016_alter_practice_practice_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='practice',
            name='practice_count',
        ),
        migrations.RemoveField(
            model_name='practice',
            name='practice_time',
        ),
    ]