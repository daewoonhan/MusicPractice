from django.db import models

class Music(models.Model):
  music_id = models.AutoField(primary_key=True)
  title = models.CharField(max_length=100)
  artist = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name='music', null=True)
  album = models.ForeignKey('Album', on_delete=models.CASCADE, related_name='music', null=True)
  play_time = models.TimeField()
  total_count = models.IntegerField()

  class Meta:
    db_table='music'

class Album(models.Model):
  album_id = models.AutoField(primary_key=True)
  album_name = models.CharField(max_length=100)
  album_cover = models.CharField(max_length=255)

  class Meta:
    db_table='album'

class Artist(models.Model):
  artist_id = models.AutoField(primary_key=True)
  artist = models.CharField(max_length=100)

  class Meta:
    db_table='artist'