from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from django.db.models import Q
from .models import Music, Album, Artist
from user.models import User
from practice.models import Practice
import jwt, datetime, pytz
from django.conf import settings
from django.db import connection

class MusicSearchView(APIView):
  def get(self, req):
    access_token = req.headers.get('Authorization')

    if not access_token or not access_token.startswith('Bearer '):
      raise AuthenticationFailed('AccessToken이 제공되지 않았습니다.')

    access_token = access_token.split(' ')[1]

    try:
      payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('토큰이 만료되었습니다.')
    except jwt.InvalidTokenError:
      raise AuthenticationFailed('유효하지 않은 토큰입니다.')

    search_query = req.query_params.get('data', None)
    if not search_query:
      return Response({
        "message": "검색어가 제공되지 않았습니다."
      }, status=400)
    
    music_results = Music.objects.filter(
        Q(title__icontains=search_query) |
        Q(artist__artist__icontains=search_query)  # artist의 이름을 참조
    ).select_related('artist', 'album').values(
        'album__album_cover', 'album__album_name', 'title', 'artist__artist', 'total_count', 'play_time'
    )

    results = list(music_results)

    response_data = {
      "message": "검색어 조회 성공",
      "data": results
    }

    return Response(response_data, status=200)

class MusicAddView(APIView):
  def post(self, req):
    access_token = req.headers.get('Authorization')

    if not access_token or not access_token.startswith('Bearer '):
      raise AuthenticationFailed('AccessToken이 제공되지 않았습니다.')

    access_token = access_token.split(' ')[1]

    try:
      payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
      user_id = payload['id']
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('토큰이 만료되었습니다.')
    except jwt.InvalidTokenError:
      raise AuthenticationFailed('유효하지 않은 토큰입니다.')

    user = User.objects.filter(id=user_id).first()
    if not user:
      raise AuthenticationFailed('존재하지 않는 사용자입니다.')

    music_id = req.data.get('music_id')
    if not music_id:
      return Response({'message': '음악 ID가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

    music = Music.objects.filter(music_id=music_id).first()
    if not music:
      return Response({'message': '음악을 찾을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    practice_date = datetime.datetime.now(pytz.timezone('Asia/Seoul')).date()

    try:
      with connection.cursor() as cursor:
        cursor.execute("""
          INSERT INTO practice (user_id, music_id, practice_date)
          VALUES (%s, %s, %s)
        """, [user.user_id, music_id, practice_date])
    except Exception as e:
      return Response({'message': f'오류 발생: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': '연습 곡 추가 성공'}, status=status.HTTP_201_CREATED)