from django.urls import path
from .views import MusicSearchView, MusicAddView

app_name = 'music'

urlpatterns = [
    path('search/', MusicSearchView.as_view()),
    path('add/', MusicAddView.as_view())
]