from django.urls import path
from . import views

urlpatterns = [
    path('', views.study_session_list, name='study_session_list'),
    path('<int:pk>/', views.study_session_detail, name='study_session_detail'),
    path('<int:pk>/start/', views.session_start, name='session_start'),
    path('<int:pk>/complete/', views.session_complete, name='session_complete'),
    path('<int:pk>/skip/', views.session_skip, name='session_skip'),
    path('today/', views.today_sessions, name='today_sessions'),
]
