from django.urls import path
from .views import PracticeListTodayView, PracticeListMonthView, RecodeTodayView, RecodeMonthView

app_name = 'practice'

urlpatterns = [
    path('toadylist/', PracticeListTodayView.as_view()),
    path('monthlylist/', PracticeListMonthView.as_view()),
    path('todayrecode/', RecodeTodayView.as_view()),
    path('monthlyrecode/', RecodeMonthView.as_view())
]