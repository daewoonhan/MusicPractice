from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import PracticeSerializer, MonthlyPracticeSerializer
from .models import Practice
import jwt
from django.conf import settings
from datetime import datetime
import pytz
from django.db import models
from user.models import User

class RecodeTodayView(APIView):
  def get(self, request):
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
      raise AuthenticationFailed('인증 토큰이 필요합니다.')

    try:
      token = auth_header.split(' ')[1]
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
      user_id = payload['id'] 
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('토큰이 만료되었습니다.')
    except jwt.DecodeError:
      raise AuthenticationFailed('유효하지 않은 토큰입니다.')

    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      raise AuthenticationFailed('존재하지 않는 사용자입니다.')
    
    today = datetime.now(pytz.timezone('Asia/Seoul')).date()

    total_practice_time = Practice.objects.filter(user=user, practice_date=today).aggregate(
      total_time=models.Sum('practice_time')
    )['total_time']

    if total_practice_time is None:
      total_practice_time = "00:00:00"

    return Response({
      "message": "오늘의 연습 시간 조회 성공",
      "data": {
        "practice_time": str(total_practice_time)
      }
    }, status=200)

class RecodeMonthView(APIView):
  def get(self, request):
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
      raise AuthenticationFailed('인증 토큰이 필요합니다.')

    try:
      token = auth_header.split(' ')[1]
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
      user_id = payload['id'] 
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('토큰이 만료되었습니다.')
    except jwt.DecodeError:
      raise AuthenticationFailed('유효하지 않은 토큰입니다.')

    first_day_of_month = datetime.now(pytz.timezone('Asia/Seoul')).replace(day=1).date()

    total_practice_time = Practice.objects.filter(user_id=user_id, practice_date__gte=first_day_of_month).aggregate(
      total_time=models.Sum('total_practice_time')
    )['total_time']

    if total_practice_time is None:
      total_practice_time = "00:00:00"

    return Response({
      "message": "이번 달 연습 시간 조회 성공",
      "data": {
        "practice_time": str(total_practice_time)
      }
    }, status=200)
    
class PracticeListTodayView(APIView):
  def get(self, request):
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
      raise AuthenticationFailed('인증 토큰이 필요합니다.')

    try:
      token = auth_header.split(' ')[1]
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
      user_id = payload['id']
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('토큰이 만료되었습니다.')
    except jwt.DecodeError:
      raise AuthenticationFailed('유효하지 않은 토큰입니다.')

    practice_records = Practice.objects.filter(user_id=user_id).values(
      'music__album_cover', 'music__title', 'music__artist', 'music__total_count',
      'music__album_name', 'music__play_time')

    practice_list = list(practice_records)

    return Response({
      "message": "연습한 곡 목록 조회 성공",
      "data": practice_list
    }, status=200)
  
class PracticeListMonthView(APIView):
  def get(self, request):
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
      raise AuthenticationFailed('인증 토큰이 필요합니다.')

    try:
      token = auth_header.split(' ')[1]
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
      user_id = payload['id']
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('토큰이 만료되었습니다.')
    except jwt.DecodeError:
      raise AuthenticationFailed('유효하지 않은 토큰입니다.')

    practice_records = Practice.objects.filter(user_id=user_id).values(
      'music__album_cover', 'music__title', 'music__artist', 'music__total_count',
      'music__album_name', 'music__play_time', 'practice_date', 'practice_count', 'total_practice_time'
    )

    practice_list = list(practice_records)

    return Response({
      "message": "연습한 곡 목록 조회 성공",
      "data": practice_list
    }, status=200)