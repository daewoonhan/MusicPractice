# Generated by Django 5.1.3 on 2024-11-27 14:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0004_album_artist_remove_music_album_cover_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='album',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='music', to='music.album'),
        ),
        migrations.AlterField(
            model_name='music',
            name='artist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='music', to='music.artist'),
        ),
    ]
