"""
Custom template tags and filters for study sessions
"""
from django import template

register = template.Library()


@register.filter(name='sum_duration')
def sum_duration(focus_sessions):
    """
    Sum the duration of all focus sessions.

    Usage: {{ session.focus_sessions.all|sum_duration }}
    """
    total = 0
    for session in focus_sessions:
        if session.duration_minutes:
            total += session.duration_minutes
    return total


@register.filter(name='progress_percent')
def progress_percent(current, total):
    """
    Calculate progress percentage.

    Usage: {{ current|progress_percent:total }}
    """
    if not total or total == 0:
        return 0
    return min(100, int((current / total) * 100))
