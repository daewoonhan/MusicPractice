from django.shortcuts import render
from rest_framework.decorators import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .serializers import UserSerializer
from .models import User, Token
import jwt, datetime, pytz

class UserRegisterView(APIView):
  def post(self, req):
    serializer = UserSerializer(data=req.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=201)

class UserLoginView(APIView):
  def post(self, req):
    id = req.data.get('id')
    password = req.data.get('password')

    if not id or not password:
      raise AuthenticationFailed('아이디와 비밀번호가 필요합니다.')

    user = User.objects.filter(id=id).first()

    if user is None:
      raise AuthenticationFailed('존재하지 않는 유저입니다.')

    if not user.check_password(password):
      raise AuthenticationFailed('비밀번호가 틀렸습니다.')

    access_payload = {
      'id': user.id,
      'exp': datetime.datetime.now(pytz.timezone('Asia/Seoul')) + datetime.timedelta(minutes=60),
      'iat': datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    }
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")

    refresh_payload = {
      'id': user.id,
      'exp': datetime.datetime.now(pytz.timezone('Asia/Seoul')) + datetime.timedelta(days=7),
      'iat': datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    }
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

    token_record, created = Token.objects.update_or_create(
    user=user,
    defaults={
      "refresh_token": refresh_token, 
      "expires_at": datetime.datetime.now(pytz.timezone('Asia/Seoul')) + datetime.timedelta(days=7)
    })

    response = Response({
      "message": "로그인 성공",
      "data": {
          "accessToken": access_token
      }
    }, status=200)

    response.set_cookie(
      key='jwt',
      value=access_token,
      httponly=True,
      secure=True,
      samesite='Strict'
    )

    return response

class UserUpdateView(APIView):
  def put(self, req):
    token = req.COOKIES.get('jwt')

    if not token:
      raise AuthenticationFailed('인증 실패')

    try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('토큰 만료')

    user = User.objects.filter(id=payload['id']).first()
    if user is None:
      raise AuthenticationFailed('존재하지 않는 유저입니다.')

    user.name = req.data.get('name', user.name)
    user.email = req.data.get('email', user.email)
    user.introduction = req.data.get('introduction', user.introduction)
    user.save()

    return Response({"message": "프로필 수정 성공"}, status=200)

class LogoutView(APIView):
  def post(self, req):
    token = req.COOKIES.get('jwt')

    if not token:
      raise AuthenticationFailed('인증 실패')

    try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
      user = User.objects.filter(id=payload['id']).first()
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('토큰 만료')

    Token.objects.filter(user=user).delete()

    res = Response()
    res.delete_cookie('jwt')
    res.data = {"message": "로그아웃 성공"}
    return res

class TokenRefreshView(APIView):
  def post(self, req):
    token = req.COOKIES.get('jwt')

    if not token:
      raise AuthenticationFailed('AccessToken이 제공되지 않았습니다.')

    try:
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('AccessToken이 만료되었습니다.')
    except jwt.InvalidTokenError:
      raise AuthenticationFailed('유효하지 않은 AccessToken입니다.')

    user = User.objects.filter(id=payload['id']).first()
    if not user:
      raise AuthenticationFailed('존재하지 않는 유저입니다.')

    token_record = Token.objects.filter(user=user).first()
    if not token_record or not token_record.refresh_token:
      raise AuthenticationFailed('Refresh Token이 없습니다.')

    try:
      jwt.decode(token_record.refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      return Response({
          "error": "refresh Token이 만료되었습니다."
      }, status=401)
    except jwt.InvalidTokenError:
      raise AuthenticationFailed('유효하지 않은 Refresh Token입니다.')

    access_payload = {
      'id': user.id,
      'exp': datetime.datetime.now(pytz.timezone('Asia/Seoul')) + datetime.timedelta(minutes=60),
      'iat': datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    }
    new_access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")

    refresh_payload = {
      'id': user.id,
      'exp': datetime.datetime.now(pytz.timezone('Asia/Seoul')) + datetime.timedelta(days=7),
      'iat': datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    }
    new_refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

    token_record.refresh_token = new_refresh_token
    token_record.expires_at = datetime.datetime.now(pytz.timezone('Asia/Seoul')) + datetime.timedelta(days=7)
    token_record.save()

    return Response({
      "message": "AccessToken 갱신 성공",
      "data": {
          "accessToken": new_access_token
      }
    }, status=200)
