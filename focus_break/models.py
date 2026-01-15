from django.db import models
from django.contrib.auth.models import User
from study_sessions.models import StudySession

class FocusModel(models.Model):
    """Predefined focus models like Pomodoro, Extended Focus, Deep Work"""
    MODEL_TYPES = [
        ('pomodoro', 'Pomodoro (25/5)'),
        ('extended', 'Extended Focus (45/10)'),
        ('deep_work', 'Deep Work (60/15)'),
    ]

    name = models.CharField(max_length=50)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES, unique=True)
    focus_duration = models.IntegerField(help_text='Focus duration in minutes')
    break_duration = models.IntegerField(help_text='Break duration in minutes')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.focus_duration}/{self.break_duration})"

class FocusSession(models.Model):
    """Individual focus session tracking"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='focus_sessions')
    study_session = models.ForeignKey(
        StudySession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='focus_sessions'
    )
    focus_model = models.ForeignKey(FocusModel, on_delete=models.SET_NULL, null=True, blank=True)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    duration_minutes = models.IntegerField(blank=True, null=True)

    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"Focus Session - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    def calculate_duration(self):
        """Calculate session duration"""
        if self.end_time and self.start_time:
            delta = self.end_time - self.start_time
            return int(delta.total_seconds() / 60)
        return None

class BreakSession(models.Model):
    """Track break sessions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='break_sessions')
    focus_session = models.ForeignKey(
        FocusSession,
        on_delete=models.CASCADE,
        related_name='breaks',
        null=True,
        blank=True
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    recommended_duration = models.IntegerField(help_text='Recommended break duration in minutes')
    actual_duration = models.IntegerField(blank=True, null=True)

    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"Break - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class UserPreference(models.Model):
    """User preferences for focus models and settings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='focus_preference')
    default_focus_model = models.ForeignKey(FocusModel, on_delete=models.SET_NULL, null=True)
    daily_study_limit = models.IntegerField(default=480, help_text='Daily study limit in minutes')
    enable_overload_alerts = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s preferences"
