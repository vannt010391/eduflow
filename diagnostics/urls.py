"""
URL configuration for diagnostics app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Diagnostic test URLs
    path('upload/<int:event_id>/', views.upload_diagnostic_test, name='diagnostic_upload'),
    path('test/<int:test_id>/', views.view_diagnostic_test, name='diagnostic_detail'),
    path('test/<int:test_id>/analyze/', views.analyze_diagnostic_test, name='diagnostic_analyze'),
    path('test/<int:test_id>/add-question/', views.add_diagnostic_question, name='diagnostic_add_question'),

    # Plan adjustment suggestion URLs
    path('suggestions/', views.list_adjustment_suggestions, name='adjustment_suggestions_list'),
    path('suggestion/<int:suggestion_id>/', views.view_adjustment_suggestion, name='adjustment_suggestion_detail'),
    path('suggestion/<int:suggestion_id>/accept/', views.accept_adjustment, name='adjustment_accept'),
    path('suggestion/<int:suggestion_id>/reject/', views.reject_adjustment, name='adjustment_reject'),
]
