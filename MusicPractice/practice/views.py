from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import PracticeSerializer, MonthlyPracticeSerializer
from .models import Practice, MonthlyPractice
import jwt
from django.conf import settings
from datetime import datetime, timedelta
import pytz
from django.db import models
from user.models import User
from django.db.models import Sum
from django.db.models.functions import TruncSecond

class RecodeTodayView(APIView):
  def get(self, request):
    auth_header = request.headers.get('Authorization', None)

    if not auth_header:
      raise AuthenticationFailed('인증 토큰이 필요합니다.')

    try:
      token = auth_header.split(' ')[1]
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('토큰이 만료되었습니다.')
    except jwt.DecodeError:
      raise AuthenticationFailed('유효하지 않은 토큰입니다.')

    try:
      user = User.objects.filter(id=payload['id']).first()
    except User.DoesNotExist:
      raise AuthenticationFailed('존재하지 않는 사용자입니다.')
    
    today = datetime.now(pytz.timezone('Asia/Seoul')).date()

    total_practice_time = Practice.objects.filter(user_id=user.user_id, practice_date=today).aggregate(
      total_time=Sum(models.Func(models.F('practice_time'), function='TIME_TO_SEC'))
    )['total_time']

    if total_practice_time is None:
      total_practice_time = "00:00:00"

    total_practice_time = str(timedelta(seconds=int(total_practice_time)))

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
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('토큰이 만료되었습니다.')
    except jwt.DecodeError:
      raise AuthenticationFailed('유효하지 않은 토큰입니다.')

    try:
      user = User.objects.filter(id=payload['id']).first()
    except User.DoesNotExist:
      raise AuthenticationFailed('존재하지 않는 사용자입니다.')

    today = datetime.now(pytz.timezone('Asia/Seoul'))
    current_month = today.strftime('%Y-%m')

    total_practice_time = MonthlyPractice.objects.filter(user_id=user.user_id, month=current_month).aggregate(
      total_time=Sum(models.Func(models.F('total_practice_time'), function='TIME_TO_SEC'))
    )['total_time']

    if total_practice_time is None:
      total_practice_time = "00:00:00"

    total_practice_time = str(timedelta(seconds=int(total_practice_time)))

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
    
    user = User.objects.filter(id=user_id).first()
    if not user:
      raise AuthenticationFailed('존재하지 않는 사용자입니다.')

    today = datetime.now(pytz.timezone('Asia/Seoul')).date()
    practice_records = Practice.objects.filter(user_id=user.user_id, practice_date=today).select_related(
      'music__album',
      'music__artist'
    ).values(
      'music__album__album_cover', 
      'music__title',          
      'music__artist__artist',   
      'music__total_count',  
      'music__album__album_name', 
      'music__play_time',  
      'practice_date',   
      'practice_count', 
      'practice_time'
    )
    
    practice_list = [
      {
        "album_cover": record['music__album__album_cover'],
        "title": record['music__title'],
        "artist": record['music__artist__artist'],
        "total_count": record['music__total_count'],
        "album_name": record['music__album__album_name'],
        "play_time": record['music__play_time'],
        "practice_date": record['practice_date'],
        "practice_count": record['practice_count'],
        "practice_time": record['practice_time']
      }
      for record in practice_records
    ]

    return Response({
      "message": "일일 연습 곡 조회 성공",
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
    
    user = User.objects.filter(id=user_id).first()
    if not user:
      raise AuthenticationFailed('존재하지 않는 사용자입니다.')

    today = datetime.now(pytz.timezone('Asia/Seoul'))
    current_month = today.strftime('%Y-%m')

    practice_records = MonthlyPractice.objects.filter(user_id=user.user_id, month=current_month
    ).select_related(
      'music__album',
      'music__artist'
    ).values(
      'music__album__album_cover', 
      'music__title',          
      'music__artist__artist',   
      'music__total_count',  
      'music__album__album_name', 
      'music__play_time',  
      'month',   
      'total_practice_count', 
      'total_practice_time'
    )
    
    practice_list = [
      {
        "album_cover": record['music__album__album_cover'],
        "title": record['music__title'],
        "artist": record['music__artist__artist'],
        "total_count": record['music__total_count'],
        "album_name": record['music__album__album_name'],
        "play_time": record['music__play_time'],
        "month": record['month'],
        "total_practice_count": record['total_practice_count'],
        "total_practice_time": record['total_practice_time']
      }
      for record in practice_records
    ]
    return Response({
      "message": "월간 연습 곡 조회 성공",
      "data": practice_list
    }, status=200)