from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer) :
  class Meta:
    model = User
    fields = ('id', 'password', 'name', 'email')

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    return user