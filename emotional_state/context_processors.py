"""
Context processor for emotional state prompting.
"""
from django.utils import timezone
from .models import EmotionalStateLog


def emotional_state_prompt(request):
    """
    Add show_emotional_prompt to context for all templates.
    Shows prompt if user is authenticated and hasn't logged today.
    """
    show_prompt = False

    if request.user.is_authenticated:
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Check if user has logged emotional state today
        today_logs = EmotionalStateLog.objects.filter(
            user=request.user,
            timestamp__gte=today_start,
            source='self_report'
        )

        # Show prompt only if no logs today
        show_prompt = not today_logs.exists()

    return {
        'show_emotional_prompt': show_prompt
    }
