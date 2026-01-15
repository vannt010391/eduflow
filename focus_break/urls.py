from django.urls import path
from . import views

urlpatterns = [
    path('timer/', views.focus_timer, name='focus_timer'),
    path('start/', views.start_focus_session, name='start_focus_session'),
    path('end/<int:pk>/', views.end_focus_session, name='end_focus_session'),
    path('break/start/', views.start_break, name='start_break'),
    path('break/end/<int:pk>/', views.end_break, name='end_break'),
    path('preferences/', views.preferences_view, name='preferences'),
]
