# Generated by Django 5.1.3 on 2024-11-28 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0015_alter_practice_practice_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='practice',
            name='practice_count',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
