from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

class Event(models.Model):
    EVENT_TYPES = [
        ('exam', 'Exam'),
        ('quiz', 'Quiz/Test'),
        ('assignment', 'Assignment Deadline'),
        ('presentation', 'Presentation'),
        ('extracurricular', 'Extracurricular Activity'),
    ]

    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_date = models.DateTimeField()
    subject = models.CharField(max_length=100)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='medium')
    estimated_prep_time = models.FloatField(help_text='Total preparation time in hours')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['event_date']

    def __str__(self):
        return f"{self.title} - {self.event_date.strftime('%Y-%m-%d')}"

    def days_until_event(self):
        delta = self.event_date - timezone.now()
        return max(0, delta.days)

    def completion_percentage(self):
        total_sessions = self.study_sessions.count()
        if total_sessions == 0:
            return 0
        completed_sessions = self.study_sessions.filter(status='completed').count()
        return int((completed_sessions / total_sessions) * 100)

    def is_at_risk(self):
        """Check if event is at risk based on completion and time remaining"""
        if self.days_until_event() <= 2 and self.completion_percentage() < 50:
            return True
        if self.days_until_event() <= 1 and self.completion_percentage() < 80:
            return True
        return False
