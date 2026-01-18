"""
Views for emotional state collection.

Supports self-reported emotional state logging via simple 3-slider form.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import EmotionalStateLog


@login_required
@require_http_methods(["GET"])
def prompt_emotional_state(request):
    """Display emotional state collection form."""
    # Check if already logged today
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_logs = EmotionalStateLog.objects.filter(
        user=request.user,
        timestamp__gte=today_start,
        source='self_report'
    )

    if today_logs.exists():
        messages.info(request, "You've already logged your emotional state today!")
        return redirect('dashboard')

    context = {
        'levels': EmotionalStateLog.LEVEL_CHOICES,
    }

    return render(request, 'emotional_state/prompt.html', context)


@login_required
@require_http_methods(["POST"])
def log_emotional_state(request):
    """Save self-reported emotional state and auto-adjust today's tasks."""
    energy = request.POST.get('energy_level')
    stress = request.POST.get('stress_level')
    focus = request.POST.get('focus_level')

    # Validate
    valid_levels = ['low', 'medium', 'high']
    if energy not in valid_levels or stress not in valid_levels or focus not in valid_levels:
        messages.error(request, "Invalid emotional state values")
        return redirect('emotional_state_prompt')

    # Create log
    log = EmotionalStateLog.objects.create(
        user=request.user,
        energy_level=energy,
        stress_level=stress,
        focus_level=focus,
        source='self_report',
        trigger_context='user_prompted'
    )

    messages.success(request, "Thank you! Your emotional state has been logged.")

    # Auto-adjust today's tasks based on emotional state
    adjusted_count = adjust_todays_tasks(request.user, log)
    if adjusted_count > 0:
        messages.info(request,
            f"We've optimized {adjusted_count} of today's study sessions based on your current state."
        )

    # Check if needs attention
    if log.needs_attention:
        messages.warning(request,
            "We noticed you might be struggling. Your study sessions have been shortened to help manage stress."
        )

    return redirect('dashboard')


def adjust_todays_tasks(user, emotional_log):
    """
    Auto-adjust today's pending study sessions based on emotional state.

    Rules:
    - High stress → Shorten sessions to 30 minutes
    - Low energy → Shorten sessions to 25 minutes
    - Low focus → Split long sessions (>45 min) into 25-minute chunks
    - Low energy + low focus → Very short sessions (20 minutes)

    Returns: Number of sessions adjusted
    """
    from study_sessions.models import StudySession
    from django.utils import timezone

    today = timezone.now().date()

    # Get today's pending sessions
    todays_sessions = StudySession.objects.filter(
        event__user=user,
        date=today,
        status='pending'
    )

    adjusted_count = 0

    for session in todays_sessions:
        original_duration = session.duration_minutes
        new_duration = original_duration
        adjustment_reason = []

        # Determine new duration based on emotional state
        if emotional_log.is_high_stress:
            new_duration = min(new_duration, 30)
            adjustment_reason.append("high stress")

        if emotional_log.is_low_energy:
            new_duration = min(new_duration, 25)
            adjustment_reason.append("low energy")

        if emotional_log.is_low_focus:
            new_duration = min(new_duration, 25)
            adjustment_reason.append("low focus")

        # Very challenging state - ultra-short sessions
        if emotional_log.is_low_energy and emotional_log.is_low_focus:
            new_duration = 20
            adjustment_reason.append("very challenging state")

        # Only update if duration changed
        if new_duration < original_duration:
            session.duration_minutes = new_duration

            # Update suggested content to reflect adjustment
            if session.suggested_content:
                session.suggested_content = (
                    f"[Adjusted for {', '.join(adjustment_reason)}] {session.suggested_content}"
                )
            else:
                session.suggested_content = f"Session adjusted for {', '.join(adjustment_reason)}"

            session.save()
            adjusted_count += 1

    return adjusted_count
