from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from datetime import timedelta
from django.utils.timezone import now

class UserManager(BaseUserManager):
  def create_user(self, id, email, password, name):      
      user = self.model(id=id, email=email, password=password, name=name)
      user.set_password(password)
      user.save(using=self._db)
      return user

class User(AbstractUser): 
  user_id = models.AutoField(primary_key=True, null=False)
  id = models.CharField(max_length=50, unique=True, null=False)
  password = models.CharField(max_length=255, null=False)
  name = models.CharField(max_length=50, null=False)
  email = models.CharField(max_length=100, unique=True, null=False)
  introduction = models.CharField(max_length=255, null=True, blank=True)

  username = None

  REQUIRED_FIELDS = []
  USERNAME_FIELD = 'id'

  objects = UserManager()

  class Meta:
    db_table='user'

class Token(models.Model):
  user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True, db_column='user_id', null=False)
  refresh_token = models.CharField(max_length=255)
  expires_at = models.DateTimeField(default=(now() + timedelta(days=7)))

  class Meta:
    db_table='token'