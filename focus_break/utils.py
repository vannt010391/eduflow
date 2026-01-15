from django.utils import timezone
from datetime import timedelta
from .models import FocusSession, BreakSession, FocusModel, UserPreference

def get_break_recommendation(user, consecutive_sessions=0, daily_minutes=0):
    """
    Calculate recommended break duration based on focus model and current state

    Args:
        user: User object
        consecutive_sessions: Number of consecutive focus sessions completed
        daily_minutes: Total minutes studied today

    Returns:
        dict with break_duration (minutes) and message
    """
    try:
        preference = UserPreference.objects.get(user=user)
        focus_model = preference.default_focus_model
    except UserPreference.DoesNotExist:
        # Default to Pomodoro if no preference set
        focus_model = FocusModel.objects.filter(model_type='pomodoro').first()

    if not focus_model:
        # Fallback to basic recommendation
        base_break = 5
    else:
        base_break = focus_model.break_duration

    # Adjust break based on consecutive sessions
    if consecutive_sessions >= 4:
        recommended_break = base_break * 3  # Long break after 4 sessions
        message = "Time for a longer break! You've completed 4 sessions."
    elif consecutive_sessions >= 2:
        recommended_break = base_break * 2  # Medium break
        message = "Take a moderate break to refresh."
    else:
        recommended_break = base_break  # Standard break
        message = "Take a short break to rest."

    # Check for overload
    daily_limit = preference.daily_study_limit if hasattr(user, 'focus_preference') else 480
    if daily_minutes >= daily_limit:
        recommended_break = 30
        message = "Warning: You've reached your daily study limit. Take a longer break!"

    return {
        'break_duration': recommended_break,
        'message': message,
        'is_overload': daily_minutes >= daily_limit
    }

def check_overload_alert(user):
    """
    Check if user should receive an overload alert

    Returns:
        dict with alert status and details
    """
    today = timezone.now().date()

    # Get today's focus sessions
    today_sessions = FocusSession.objects.filter(
        user=user,
        start_time__date=today,
        completed=True
    )

    total_minutes = sum(s.duration_minutes or 0 for s in today_sessions)

    try:
        preference = UserPreference.objects.get(user=user)
        daily_limit = preference.daily_study_limit
        enabled = preference.enable_overload_alerts
    except UserPreference.DoesNotExist:
        daily_limit = 480  # 8 hours default
        enabled = True

    alert = False
    message = ""

    if enabled and total_minutes >= daily_limit:
        alert = True
        message = f"You've studied {total_minutes} minutes today. Consider taking a longer break!"
    elif enabled and total_minutes >= daily_limit * 0.8:
        alert = True
        message = f"You're approaching your daily study limit ({total_minutes}/{daily_limit} minutes)."

    return {
        'alert': alert,
        'message': message,
        'total_minutes': total_minutes,
        'daily_limit': daily_limit,
        'percentage': int((total_minutes / daily_limit) * 100) if daily_limit > 0 else 0
    }

def get_consecutive_sessions(user):
    """Get count of consecutive completed focus sessions today"""
    today = timezone.now().date()

    recent_sessions = FocusSession.objects.filter(
        user=user,
        start_time__date=today
    ).order_by('-start_time')[:10]

    consecutive = 0
    for session in recent_sessions:
        if session.completed:
            consecutive += 1
        else:
            break

    return consecutive
