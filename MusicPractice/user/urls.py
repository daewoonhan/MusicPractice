from django.urls import path
from .views import UserRegisterView, UserLoginView, UserUpdateView, LogoutView, TokenRefreshView

app_name = 'user'

urlpatterns = [
    path('login/', UserLoginView.as_view()),
    path('signup/', UserRegisterView.as_view()),
    path('profile/', UserUpdateView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('refresh/', TokenRefreshView.as_view())
]