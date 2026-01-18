"""
Diagnostic Test models for error analysis and targeted review.

Supports:
- PDF upload or manual question entry
- AI-powered error analysis
- Plan adjustment suggestions
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class DiagnosticTest(models.Model):
    """
    A diagnostic test associated with an Event.

    Each Event can have zero or one DiagnosticTest.
    Test contains questions with user answers for error analysis.
    """

    event = models.OneToOneField(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='diagnostic_test'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diagnostic_tests')

    title = models.CharField(max_length=200)
    uploaded_file = models.FileField(
        upload_to='diagnostics/',
        blank=True,
        null=True,
        help_text='PDF file of diagnostic test (optional)'
    )

    # Analysis results (JSON following strict schema)
    analysis_result = models.JSONField(
        blank=True,
        null=True,
        help_text='AI analysis result: {"error_groups": [...]}'
    )
    analyzed_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Diagnostic Test'
        verbose_name_plural = 'Diagnostic Tests'

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    @property
    def total_questions(self):
        """Total number of questions in this test"""
        return self.questions.count()

    @property
    def correct_count(self):
        """Number of correct answers"""
        return self.questions.filter(is_correct=True).count()

    @property
    def incorrect_count(self):
        """Number of incorrect answers"""
        return self.questions.filter(is_correct=False).count()

    @property
    def score_percentage(self):
        """Score as percentage"""
        if self.total_questions == 0:
            return 0
        return int((self.correct_count / self.total_questions) * 100)

    @property
    def is_analyzed(self):
        """Check if test has been analyzed by AI"""
        return self.analysis_result is not None and self.analyzed_at is not None

    @property
    def error_groups(self):
        """Get error groups from analysis result"""
        if not self.is_analyzed:
            return []
        return self.analysis_result.get('error_groups', [])


class DiagnosticQuestion(models.Model):
    """
    Individual question in a diagnostic test.

    Stores both correct and user answers for error analysis.
    """

    ERROR_TYPE_CHOICES = [
        ('conceptual', 'Conceptual Error'),
        ('application', 'Application Error'),
        ('reasoning', 'Reasoning Error'),
    ]

    diagnostic_test = models.ForeignKey(
        DiagnosticTest,
        on_delete=models.CASCADE,
        related_name='questions'
    )

    question_number = models.IntegerField(help_text='Question number in the test')
    question_text = models.TextField()
    correct_answer = models.TextField()
    user_answer = models.TextField()
    topic = models.CharField(max_length=200, blank=True, help_text='Subject topic (optional)')

    # Analysis fields (populated by AI)
    is_correct = models.BooleanField(default=False)
    error_type = models.CharField(
        max_length=20,
        choices=ERROR_TYPE_CHOICES,
        blank=True,
        help_text='Type of error if answer is incorrect'
    )

    class Meta:
        ordering = ['question_number']
        unique_together = ['diagnostic_test', 'question_number']
        verbose_name = 'Diagnostic Question'
        verbose_name_plural = 'Diagnostic Questions'

    def __str__(self):
        status = "✓" if self.is_correct else "✗"
        return f"Q{self.question_number} {status} - {self.topic or 'General'}"

    def save(self, *args, **kwargs):
        """Auto-check correctness on save"""
        # Simple correctness check (case-insensitive, whitespace-normalized)
        self.is_correct = (
            self.correct_answer.strip().lower() == self.user_answer.strip().lower()
        )
        super().save(*args, **kwargs)


class PlanAdjustmentSuggestion(models.Model):
    """
    AI-generated plan adjustment suggestion.

    Triggered by:
    - High stress
    - Repeated overruns
    - At-risk events
    - Diagnostic error concentration

    IMPORTANT: Requires user confirmation - no automatic changes.
    """

    ADJUSTMENT_TYPE_CHOICES = [
        ('split', 'Split Task'),
        ('shorten', 'Shorten Duration'),
        ('reorder', 'Reorder Tasks'),
        ('focus_mode_change', 'Change Focus Mode'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adjustment_suggestions')
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='adjustment_suggestions'
    )

    # Trigger context
    triggered_by = models.CharField(
        max_length=100,
        help_text='What triggered this suggestion (e.g., high_stress, at_risk, overrun)'
    )
    triggered_at = models.DateTimeField(auto_now_add=True)

    # AI suggestion data (JSON following strict schema)
    context = models.JSONField(
        help_text='Context: emotional_state, dominant_error_topic, etc.'
    )
    adjustments = models.JSONField(
        help_text='List of suggested adjustments with details'
    )
    rationale = models.TextField(
        help_text='AI explanation for these suggestions (MANDATORY)'
    )

    # User decision
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)
    user_notes = models.TextField(
        blank=True,
        help_text='User notes on why they accepted/rejected'
    )

    class Meta:
        ordering = ['-triggered_at']
        verbose_name = 'Plan Adjustment Suggestion'
        verbose_name_plural = 'Plan Adjustment Suggestions'

    def __str__(self):
        return f"{self.event.title} - {self.triggered_by} ({self.status})"

    @property
    def is_pending(self):
        """Check if suggestion is awaiting user decision"""
        return self.status == 'pending'

    @property
    def is_accepted(self):
        """Check if user accepted the suggestion"""
        return self.status == 'accepted'

    @property
    def is_rejected(self):
        """Check if user rejected the suggestion"""
        return self.status == 'rejected'

    @property
    def adjustment_count(self):
        """Number of suggested adjustments"""
        return len(self.adjustments) if self.adjustments else 0

    def accept(self, user_notes=''):
        """Mark suggestion as accepted"""
        self.status = 'accepted'
        self.reviewed_at = timezone.now()
        self.user_notes = user_notes
        self.save()

    def reject(self, user_notes=''):
        """Mark suggestion as rejected"""
        self.status = 'rejected'
        self.reviewed_at = timezone.now()
        self.user_notes = user_notes
        self.save()
