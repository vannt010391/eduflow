from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import StudySession
from .forms import StudySessionUpdateForm
from focus_break.models import FocusSession

@login_required
def study_session_list(request):
    """List all study sessions for the logged-in user"""
    today = timezone.now().date()
    upcoming_sessions = StudySession.objects.filter(
        event__user=request.user,
        date__gte=today,
        status='pending'
    ).order_by('date', 'start_time')[:10]

    past_sessions = StudySession.objects.filter(
        event__user=request.user,
        date__lt=today
    ).order_by('-date', '-start_time')[:20]

    context = {
        'upcoming_sessions': upcoming_sessions,
        'past_sessions': past_sessions,
    }

    return render(request, 'study_sessions/session_list.html', context)

@login_required
def study_session_detail(request, pk):
    """View details of a specific study session"""
    session = get_object_or_404(StudySession, pk=pk, event__user=request.user)

    if request.method == 'POST':
        form = StudySessionUpdateForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            messages.success(request, 'Study session updated successfully!')
            return redirect('study_session_detail', pk=pk)
    else:
        form = StudySessionUpdateForm(instance=session)

    context = {
        'session': session,
        'form': form,
    }

    return render(request, 'study_sessions/session_detail.html', context)

@login_required
def session_start(request, pk):
    """Start a study session timer"""
    session = get_object_or_404(StudySession, pk=pk, event__user=request.user)

    if not session.actual_start_time:
        session.actual_start_time = timezone.now()
        session.status = 'in_progress'
        session.save()
        messages.success(request, 'Study session started! Focus on your work.')
    else:
        messages.warning(request, 'This session has already been started.')

    return redirect('study_session_detail', pk=pk)

@login_required
def session_complete(request, pk):
    """Mark a study session as complete"""
    session = get_object_or_404(StudySession, pk=pk, event__user=request.user)

    if session.actual_start_time and not session.actual_end_time:
        session.actual_end_time = timezone.now()
        session.actual_duration_minutes = session.calculate_actual_duration()
        session.status = 'completed'
        session.save()
        messages.success(request, f'Great work! Session completed in {session.actual_duration_minutes} minutes.')
    elif not session.actual_start_time:
        session.status = 'completed'
        session.save()
        messages.success(request, 'Session marked as completed.')
    else:
        messages.warning(request, 'This session has already been completed.')

    return redirect('event_detail', pk=session.event.pk)

@login_required
def session_skip(request, pk):
    """Mark a study session as skipped"""
    session = get_object_or_404(StudySession, pk=pk, event__user=request.user)
    session.status = 'skipped'
    session.save()
    messages.info(request, 'Session marked as skipped.')
    return redirect('event_detail', pk=session.event.pk)

@login_required
def today_sessions(request):
    """View today's study sessions"""
    today = timezone.now().date()
    sessions = StudySession.objects.filter(
        event__user=request.user,
        date=today
    ).order_by('start_time')

    context = {
        'sessions': sessions,
        'today': today,
    }

    return render(request, 'study_sessions/today_sessions.html', context)
