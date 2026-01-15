from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q
from datetime import timedelta
from events.models import Event
from study_sessions.models import StudySession
from focus_break.models import FocusSession

@login_required
def analytics_dashboard(request):
    """Main analytics dashboard showing user study metrics"""
    user = request.user
    today = timezone.now().date()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    # Daily metrics
    today_sessions = StudySession.objects.filter(
        event__user=user,
        date=today
    )
    today_completed = today_sessions.filter(status='completed').count()
    today_total = today_sessions.count()

    # Focus sessions today
    today_focus = FocusSession.objects.filter(
        user=user,
        start_time__date=today,
        completed=True
    )
    today_focus_minutes = sum(s.duration_minutes or 0 for s in today_focus)

    # Weekly metrics
    week_sessions = StudySession.objects.filter(
        event__user=user,
        date__range=[week_start, week_end]
    )
    week_completed = week_sessions.filter(status='completed').count()
    week_total = week_sessions.count()

    # Weekly focus time
    week_focus = FocusSession.objects.filter(
        user=user,
        start_time__date__range=[week_start, week_end],
        completed=True
    )
    week_focus_minutes = sum(s.duration_minutes or 0 for s in week_focus)

    # Events metrics
    total_events = Event.objects.filter(user=user).count()
    upcoming_events = Event.objects.filter(user=user, event_date__gte=timezone.now()).count()
    past_events = Event.objects.filter(user=user, event_date__lt=timezone.now())

    # Calculate events completed on time (past events with >80% completion)
    events_on_time = sum(1 for e in past_events if e.completion_percentage() >= 80)
    total_past_events = past_events.count()

    # Events at risk
    at_risk_events = [e for e in Event.objects.filter(user=user, event_date__gte=timezone.now()) if e.is_at_risk()]

    # Calculate average daily study time (last 7 days)
    last_7_days = [today - timedelta(days=i) for i in range(7)]
    daily_study_times = []

    for day in last_7_days:
        day_focus = FocusSession.objects.filter(
            user=user,
            start_time__date=day,
            completed=True
        )
        minutes = sum(s.duration_minutes or 0 for s in day_focus)
        daily_study_times.append(minutes)

    avg_daily_minutes = sum(daily_study_times) / len(daily_study_times) if daily_study_times else 0

    # Consistency score (days with study activity in last 7 days)
    days_with_activity = sum(1 for minutes in daily_study_times if minutes > 0)
    consistency_score = int((days_with_activity / 7) * 100)

    # Session duration analysis
    all_focus_sessions = FocusSession.objects.filter(user=user, completed=True)
    if all_focus_sessions.exists():
        avg_session_duration = sum(s.duration_minutes or 0 for s in all_focus_sessions) / all_focus_sessions.count()
    else:
        avg_session_duration = 0

    # Overlong sessions (>90 minutes)
    overlong_sessions = FocusSession.objects.filter(
        user=user,
        completed=True,
        duration_minutes__gt=90
    ).count()

    context = {
        # Today
        'today_completed': today_completed,
        'today_total': today_total,
        'today_focus_minutes': today_focus_minutes,
        'today_focus_hours': round(today_focus_minutes / 60, 1),

        # This week
        'week_completed': week_completed,
        'week_total': week_total,
        'week_focus_minutes': week_focus_minutes,
        'week_focus_hours': round(week_focus_minutes / 60, 1),
        'week_start': week_start,
        'week_end': week_end,

        # Events
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'events_on_time': events_on_time,
        'total_past_events': total_past_events,
        'at_risk_events': at_risk_events,
        'on_time_percentage': int((events_on_time / total_past_events * 100)) if total_past_events > 0 else 0,

        # Effectiveness
        'avg_daily_minutes': int(avg_daily_minutes),
        'avg_daily_hours': round(avg_daily_minutes / 60, 1),
        'consistency_score': consistency_score,
        'avg_session_duration': int(avg_session_duration),
        'overlong_sessions': overlong_sessions,

        # Chart data for last 7 days
        'daily_labels': [day.strftime('%a') for day in reversed(last_7_days)],
        'daily_minutes': list(reversed(daily_study_times)),
        'daily_data': list(zip(
            [day.strftime('%a') for day in reversed(last_7_days)],
            list(reversed(daily_study_times))
        )),
    }

    return render(request, 'analytics/dashboard.html', context)

@login_required
def dashboard_home(request):
    """Home dashboard showing today's tasks and overview"""
    user = request.user
    today = timezone.now().date()

    # Today's study sessions
    today_sessions = StudySession.objects.filter(
        event__user=user,
        date=today
    ).order_by('start_time')

    # Upcoming events (next 7 days)
    next_week = today + timedelta(days=7)
    upcoming_events = Event.objects.filter(
        user=user,
        event_date__range=[timezone.now(), timezone.make_aware(timezone.datetime.combine(next_week, timezone.datetime.max.time()))]
    ).order_by('event_date')[:5]

    # Events at risk
    at_risk_events = [e for e in upcoming_events if e.is_at_risk()]

    # Today's focus time
    today_focus = FocusSession.objects.filter(
        user=user,
        start_time__date=today,
        completed=True
    )
    today_focus_minutes = sum(s.duration_minutes or 0 for s in today_focus)

    # Active focus session
    active_focus = FocusSession.objects.filter(
        user=user,
        completed=False,
        end_time__isnull=True
    ).first()

    context = {
        'today_sessions': today_sessions,
        'upcoming_events': upcoming_events,
        'at_risk_events': at_risk_events,
        'today_focus_minutes': today_focus_minutes,
        'active_focus': active_focus,
        'today': today,
    }

    return render(request, 'analytics/home.html', context)
