from django.db import models
from events.models import Event
from django.utils import timezone

class StudySession(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped'),
        ('postponed', 'Postponed'),
        ('in_progress', 'In Progress'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='study_sessions')
    date = models.DateField()
    start_time = models.TimeField()
    duration_minutes = models.IntegerField(help_text='Planned duration in minutes')
    suggested_content = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Actual tracking
    actual_start_time = models.DateTimeField(blank=True, null=True)
    actual_end_time = models.DateTimeField(blank=True, null=True)
    actual_duration_minutes = models.IntegerField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.event.title} - {self.date} at {self.start_time}"

    def is_overdue(self):
        """Check if session is past its scheduled time and not completed"""
        if self.status in ['completed', 'skipped']:
            return False
        session_datetime = timezone.make_aware(
            timezone.datetime.combine(self.date, self.start_time)
        )
        return timezone.now() > session_datetime

    def calculate_actual_duration(self):
        """Calculate actual duration if start and end times are set"""
        if self.actual_start_time and self.actual_end_time:
            delta = self.actual_end_time - self.actual_start_time
            return int(delta.total_seconds() / 60)
        return None

    def get_total_focus_time(self):
        """Calculate total time from all completed focus sessions"""
        return sum(
            fs.duration_minutes or 0
            for fs in self.focus_sessions.filter(completed=True)
        )

    def get_progress_percent(self):
        """Calculate progress percentage based on focus sessions"""
        total_focus = self.get_total_focus_time()
        if self.duration_minutes and self.duration_minutes > 0:
            return min(100, int((total_focus / self.duration_minutes) * 100))
        return 0

    def is_target_reached(self):
        """Check if total focus time meets or exceeds target duration"""
        return self.get_total_focus_time() >= self.duration_minutes
