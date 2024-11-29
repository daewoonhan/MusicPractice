from django.urls import path
from .views import PracticeListTodayView, PracticeListMonthView, RecodeTodayView, RecodeMonthView

app_name = 'practice'

urlpatterns = [
    path('todaylist/', PracticeListTodayView.as_view()),
    path('monthlist/', PracticeListMonthView.as_view()),
    path('todayrecode/', RecodeTodayView.as_view()),
    path('monthrecode/', RecodeMonthView.as_view())
]