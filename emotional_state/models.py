"""
Emotional State models for tracking learning-related emotional dimensions.

IMPORTANT: Only tracks 3 dimensions (energy, stress, focus) - no other psychological data.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class EmotionalStateLog(models.Model):
    """
    Records user's learning-related emotional state.

    Supports:
    - Self-reported states (user input)
    - Inferred states (from behavior patterns)

    STRICT: Only 3 dimensions allowed (energy, stress, focus)
    """

    SOURCE_CHOICES = [
        ('self_report', 'Self-Reported'),
        ('inferred', 'Inferred from Behavior'),
    ]

    LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    # Core fields
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emotional_logs')
    timestamp = models.DateTimeField(auto_now_add=True)

    # Emotional dimensions (STRICT - only these 3)
    energy_level = models.CharField(
        max_length=10,
        choices=LEVEL_CHOICES,
        help_text='Physical/mental energy level'
    )
    stress_level = models.CharField(
        max_length=10,
        choices=LEVEL_CHOICES,
        help_text='Study-related stress level'
    )
    focus_level = models.CharField(
        max_length=10,
        choices=LEVEL_CHOICES,
        help_text='Ability to concentrate'
    )

    # Metadata
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        help_text='How this state was captured'
    )
    trigger_context = models.CharField(
        max_length=100,
        blank=True,
        help_text='What triggered this log (e.g., session_end, day_start)'
    )

    # Optional: Link to study session if triggered by session end
    study_session = models.ForeignKey(
        'study_sessions.StudySession',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='emotional_logs'
    )

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['source', '-timestamp']),
        ]
        verbose_name = 'Emotional State Log'
        verbose_name_plural = 'Emotional State Logs'

    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')} ({self.source})"

    @property
    def is_high_stress(self):
        """Check if stress level is high"""
        return self.stress_level == 'high'

    @property
    def is_low_energy(self):
        """Check if energy level is low"""
        return self.energy_level == 'low'

    @property
    def is_low_focus(self):
        """Check if focus level is low"""
        return self.focus_level == 'low'

    @property
    def needs_attention(self):
        """Check if this state suggests user needs help"""
        return self.is_high_stress or (self.is_low_energy and self.is_low_focus)

    @classmethod
    def get_recent_state(cls, user, days=7):
        """Get user's recent emotional state average"""
        recent_logs = cls.objects.filter(
            user=user,
            timestamp__gte=timezone.now() - timezone.timedelta(days=days)
        )

        if not recent_logs.exists():
            return None

        # Calculate averages
        level_to_num = {'low': 1, 'medium': 2, 'high': 3}

        avg_energy = sum(level_to_num[log.energy_level] for log in recent_logs) / recent_logs.count()
        avg_stress = sum(level_to_num[log.stress_level] for log in recent_logs) / recent_logs.count()
        avg_focus = sum(level_to_num[log.focus_level] for log in recent_logs) / recent_logs.count()

        num_to_level = lambda x: 'low' if x < 1.7 else 'medium' if x < 2.4 else 'high'

        return {
            'energy': num_to_level(avg_energy),
            'stress': num_to_level(avg_stress),
            'focus': num_to_level(avg_focus),
            'sample_size': recent_logs.count()
        }
