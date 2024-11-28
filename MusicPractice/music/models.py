from django.db import models

class Music(models.Model):
  music_id = models.AutoField(primary_key=True, null=False)
  title = models.CharField(max_length=100, db_index=True, null=False)
  artist = models.ForeignKey('Artist', on_delete=models.CASCADE, related_name='music', null=True)
  album = models.ForeignKey('Album', on_delete=models.CASCADE, related_name='music', null=True)
  play_time = models.TimeField(null=False)
  total_count = models.IntegerField(null=False)

  class Meta:
    db_table='music'

class Album(models.Model):
  album_id = models.AutoField(primary_key=True, null=False)
  album_name = models.CharField(max_length=100, null=False)
  album_cover = models.CharField(max_length=255, null=False)

  class Meta:
    db_table='album'

class Artist(models.Model):
  artist_id = models.AutoField(primary_key=True, null=False)
  artist = models.CharField(max_length=100, db_index=True, null=False)

  class Meta:
    db_table='artist'