from rest_framework import serializers
from .models import Practice, MonthlyPractice

class PracticeSerializer(serializers.ModelSerializer) :
  class Meta:
    model = Practice
    fields = '__all__'

class MonthlyPracticeSerializer(serializers.ModelSerializer) :
  class Meta:
    model = MonthlyPractice
    fields = '__all__'