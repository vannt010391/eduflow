from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class DailyStudyLog(models.Model):
    """Track daily study statistics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField()
    total_focus_minutes = models.IntegerField(default=0)
    total_sessions = models.IntegerField(default=0)
    completed_sessions = models.IntegerField(default=0)
    skipped_sessions = models.IntegerField(default=0)
    average_session_duration = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class WeeklyStudyLog(models.Model):
    """Track weekly study statistics"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_logs')
    week_start = models.DateField()
    week_end = models.DateField()
    total_focus_minutes = models.IntegerField(default=0)
    total_sessions = models.IntegerField(default=0)
    completed_sessions = models.IntegerField(default=0)
    events_completed = models.IntegerField(default=0)
    events_total = models.IntegerField(default=0)
    consistency_score = models.FloatField(default=0, help_text='Percentage of days with study activity')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'week_start']
        ordering = ['-week_start']

    def __str__(self):
        return f"{self.user.username} - Week {self.week_start} to {self.week_end}"
