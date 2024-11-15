# exam/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('start-exam/', views.start_exam, name='start_exam'),
    path('speech-input/', views.speech_input, name='speech_input'),
    path('preview-answer/', views.preview_answer, name='preview_answer'),
    path('save-answer/', views.save_answer, name='save_answer'),
    path('submit-all-answers/', views.submit_all_answers, name='submit_all_answers'),
]
