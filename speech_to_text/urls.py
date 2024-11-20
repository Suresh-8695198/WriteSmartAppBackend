from django.urls import path
from . import views

urlpatterns = [
    path('fetch-questions/', views.fetch_questions, name='fetch_questions'),
    path('speech-to-text/', views.speech_to_text, name='speech_to_text'),
    path('save-answer/', views.save_answer, name='save_answer'),
]
