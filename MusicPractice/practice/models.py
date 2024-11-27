from django.db import models

class Practice(models.Model):
  practice_id = models.AutoField(primary_key=True)
  music = models.ForeignKey('music.Music', on_delete=models.CASCADE)
  user = models.ForeignKey('user.User', on_delete=models.CASCADE)
  practice_date = models.DateField()

  class Meta:
    db_table='practice'

class MonthlyPractice(models.Model):
  month_id = models.AutoField(primary_key=True)
  music = models.ForeignKey('music.Music', on_delete=models.CASCADE)
  user = models.ForeignKey('user.User', on_delete=models.CASCADE)
  month = models.CharField(max_length=7)
  total_practice_count = models.IntegerField(default=0)
  total_practice_time = models.TimeField()

  class Meta:
    db_table='monthly_practice'
    unique_together = ('month', 'music', 'user')