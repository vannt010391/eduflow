"""
URL configuration for emotional state app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.prompt_emotional_state, name='emotional_state_prompt'),
    path('log/submit/', views.log_emotional_state, name='emotional_state_submit'),
]
