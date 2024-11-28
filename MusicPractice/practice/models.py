from django.db import models

class Practice(models.Model):
  practice_id = models.AutoField(primary_key=True, null=False)
  music = models.ForeignKey('music.Music', on_delete=models.CASCADE, null=False)
  user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=False)
  practice_date = models.DateField()
  practice_count = models.IntegerField(default=0)
  practice_time = models.TimeField()

  class Meta:
    db_table='practice'
    unique_together = ('practice_date', 'music', 'user')

class MonthlyPractice(models.Model):
  month_id = models.AutoField(primary_key=True)
  music = models.ForeignKey('music.Music', on_delete=models.CASCADE, null=False)
  user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=False)
  month = models.CharField(max_length=7)
  total_practice_count = models.IntegerField(default=0)
  total_practice_time = models.TimeField()

  class Meta:
    db_table='monthly_practice'
    unique_together = ('month', 'music', 'user')