"""
Integration layer between AI services and Event/StudySession models.

This module provides helper functions to integrate AI-generated learning plans
into the existing EduFlow AI system without modifying core business logic.
"""
import logging
from datetime import datetime, timedelta, time
from typing import List, Optional

from django.db import transaction
from django.utils import timezone

from events.models import Event
from study_sessions.models import StudySession
from focus_break.models import UserPreference, FocusModel
from .services import get_ai_service
from .schemas import LearningPlan, LearningTask

logger = logging.getLogger(__name__)


# Mapping from AI task types to focus durations
TASK_TYPE_TO_DURATION = {
    'concept_review': 30,  # Lighter cognitive load
    'practice': 45,  # Medium intensity
    'deep_practice': 60,  # Maximum focus required
    'revision': 30,  # Review is lighter
    'mock_test': 60,  # Full simulation
}

# Mapping from AI difficulty to priority boost
DIFFICULTY_TO_PRIORITY_BOOST = {
    'low': 0,
    'medium': 1,
    'high': 2,
}


def generate_ai_study_sessions(
    event: Event,
    force_regenerate: bool = False
) -> List[StudySession]:
    """
    Generate AI-powered study sessions for an event.

    This implements the integration of AI Use Case #1: Event → Learning Plan Generation

    Args:
        event: Event model instance
        force_regenerate: Force new AI generation even if cached

    Returns:
        List of created StudySession instances
    """
    # Get user preferences for context
    try:
        user_pref = UserPreference.objects.get(user=event.user)
        daily_limit = user_pref.daily_study_limit
        focus_model_name = user_pref.default_focus_model.name if user_pref.default_focus_model else "Pomodoro"
    except UserPreference.DoesNotExist:
        daily_limit = 480  # 8 hours default
        focus_model_name = "Pomodoro"

    # Call AI service
    ai_service = get_ai_service()
    learning_plan = ai_service.generate_learning_plan(
        event_title=event.title,
        event_type=event.event_type,
        event_date=event.event_date,
        prep_time_hours=event.estimated_prep_time,
        subject=event.subject,
        description=event.description or "",
        daily_limit_minutes=daily_limit,
        focus_mode=focus_model_name,
        force_regenerate=force_regenerate
    )

    # If AI fails or is disabled, return empty list (caller can fall back to deterministic)
    if not learning_plan:
        logger.info(f"AI plan generation skipped for event '{event.title}', using deterministic fallback")
        return []

    # Generate study sessions from AI plan
    sessions = _create_sessions_from_plan(event, learning_plan)

    logger.info(
        f"Created {len(sessions)} AI-powered study sessions for event '{event.title}'"
    )

    return sessions


def _create_sessions_from_plan(
    event: Event,
    plan: LearningPlan
) -> List[StudySession]:
    """
    Create StudySession instances from an AI-generated learning plan.

    Args:
        event: Event model instance
        plan: AI-generated LearningPlan

    Returns:
        List of created StudySession instances
    """
    sessions = []
    tasks: List[LearningTask] = plan['tasks']

    # Calculate scheduling parameters
    days_until_event = (event.event_date.date() - timezone.now().date()).days

    # If event is in the past or today, schedule sessions for upcoming days anyway
    # This ensures users can still benefit from AI-generated study plans
    if days_until_event <= 0:
        logger.info(f"Event '{event.title}' is today or in the past, scheduling sessions for next 7 days")
        days_until_event = 7  # Default to 7 days for planning

    # Get user's daily study limit
    try:
        user_pref = UserPreference.objects.get(user=event.user)
        daily_limit_minutes = user_pref.daily_study_limit
    except UserPreference.DoesNotExist:
        daily_limit_minutes = 480

    # Calculate total minutes needed
    total_minutes = sum(task['suggested_duration_minutes'] for task in tasks)

    # Distribute sessions across available days
    # Try to respect daily limit while fitting all tasks
    sessions_per_day = _calculate_sessions_per_day(
        total_minutes=total_minutes,
        days_available=days_until_event,
        daily_limit_minutes=daily_limit_minutes
    )

    # Create sessions
    current_date = timezone.now().date()
    task_index = 0
    sessions_created_today = 0

    with transaction.atomic():
        for day_offset in range(days_until_event):
            session_date = current_date + timedelta(days=day_offset)

            # How many sessions to create on this day
            sessions_for_today = min(sessions_per_day, len(tasks) - task_index)

            for session_num in range(sessions_for_today):
                if task_index >= len(tasks):
                    break

                task = tasks[task_index]

                # Calculate start time (stagger sessions by 2 hours if multiple per day)
                base_hour = 18  # 6 PM default
                session_start_hour = base_hour + (session_num * 2)
                if session_start_hour > 22:  # Don't schedule too late
                    session_start_hour = 22

                start_time = time(hour=session_start_hour, minute=0)

                # Create the session
                session = StudySession.objects.create(
                    event=event,
                    date=session_date,
                    start_time=start_time,
                    duration_minutes=task['suggested_duration_minutes'],
                    suggested_content=_format_task_content(task, task_index + 1, len(tasks)),
                    status='pending',
                    notes=task.get('notes', '')
                )

                sessions.append(session)
                task_index += 1
                sessions_created_today += 1

            # Reset counter for next day
            sessions_created_today = 0

    return sessions


def _calculate_sessions_per_day(
    total_minutes: int,
    days_available: int,
    daily_limit_minutes: int
) -> int:
    """
    Calculate optimal number of sessions per day.

    Args:
        total_minutes: Total study time needed
        days_available: Days until event
        daily_limit_minutes: User's daily study limit

    Returns:
        Number of sessions to schedule per day
    """
    # Calculate average minutes per day needed
    avg_minutes_per_day = total_minutes / days_available

    # If it fits within daily limit, great
    if avg_minutes_per_day <= daily_limit_minutes:
        # Assume average session is 40 minutes
        return max(1, int(avg_minutes_per_day / 40))

    # Otherwise, max out at daily limit
    return max(1, int(daily_limit_minutes / 40))


def _format_task_content(
    task: LearningTask,
    task_number: int,
    total_tasks: int
) -> str:
    """
    Format AI task data into human-readable suggested content.

    Args:
        task: AI-generated task
        task_number: Current task number
        total_tasks: Total number of tasks

    Returns:
        Formatted content string
    """
    content_parts = [
        f"Task {task_number}/{total_tasks}: {task['title']}",
        f"",
        f"Type: {task['task_type'].replace('_', ' ').title()}",
        f"Difficulty: {task['difficulty'].title()}",
        f"Duration: {task['suggested_duration_minutes']} minutes",
    ]

    if task.get('notes'):
        content_parts.extend([
            f"",
            f"Tips:",
            task['notes']
        ])

    return "\n".join(content_parts)


def check_for_replan_triggers(event: Event) -> Optional[str]:
    """
    Check if an event should trigger adaptive re-planning.

    This implements part of AI Use Case #3: Adaptive Re-Planning

    Args:
        event: Event to check

    Returns:
        Issue type string if re-planning needed, None otherwise
        Values: 'tasks_overrunning', 'tasks_skipped', 'event_at_risk'
    """
    sessions = event.study_sessions.all()

    if not sessions:
        return None

    # Check for tasks overrunning
    completed_sessions = sessions.filter(status='completed', actual_duration_minutes__isnull=False)
    if completed_sessions.count() >= 3:  # Need enough data
        overrun_count = 0
        total_count = 0

        for session in completed_sessions:
            if session.actual_duration_minutes > session.duration_minutes * 1.2:  # 20% over
                overrun_count += 1
            total_count += 1

        if overrun_count / total_count >= 0.5:  # 50% of sessions overrunning
            return 'tasks_overrunning'

    # Check for skipped tasks
    skipped_count = sessions.filter(status='skipped').count()
    total_sessions = sessions.count()

    if skipped_count >= 3 and skipped_count / total_sessions >= 0.3:  # 30% skipped
        return 'tasks_skipped'

    # Check if event is at risk
    if event.is_at_risk():
        return 'event_at_risk'

    return None


def generate_replan_suggestions(event: Event, issue_type: str):
    """
    Generate AI-powered re-planning suggestions for an event.

    This implements AI Use Case #3: Adaptive Re-Planning

    Args:
        event: Event to generate suggestions for
        issue_type: Type of issue ('tasks_overrunning', 'tasks_skipped', 'event_at_risk')

    Returns:
        Dict with suggestions, or None if AI fails
    """
    # Gather data about current tasks
    sessions = event.study_sessions.all()
    tasks_data = []

    for session in sessions:
        task_dict = {
            'title': session.suggested_content.split('\n')[0] if session.suggested_content else 'Untitled',
            'planned_duration': session.duration_minutes,
            'actual_duration': session.actual_duration_minutes,
            'status': session.status,
        }
        tasks_data.append(task_dict)

    # Gather performance data
    completed_sessions = sessions.filter(status='completed')
    total_actual = sum(s.actual_duration_minutes or 0 for s in completed_sessions)
    total_planned = sum(s.duration_minutes for s in completed_sessions)

    performance_data = {
        'avg_overrun_percent': ((total_actual - total_planned) / total_planned * 100) if total_planned > 0 else 0,
        'skipped_count': sessions.filter(status='skipped').count(),
        'completion_percent': event.completion_percentage(),
        'days_remaining': event.days_until_event(),
    }

    # Call AI service
    ai_service = get_ai_service()
    suggestions = ai_service.suggest_replan(
        event_title=event.title,
        tasks_data=tasks_data,
        issue_type=issue_type,
        performance_data=performance_data
    )

    return suggestions
