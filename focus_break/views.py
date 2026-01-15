from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import FocusSession, BreakSession, FocusModel, UserPreference
from .utils import get_break_recommendation, check_overload_alert, get_consecutive_sessions

@login_required
def focus_timer(request):
    """Main focus timer view"""
    focus_models = FocusModel.objects.all()

    # Get or create user preference
    preference, created = UserPreference.objects.get_or_create(
        user=request.user,
        defaults={'default_focus_model': focus_models.first()}
    )

    # Get active session if exists
    active_session = FocusSession.objects.filter(
        user=request.user,
        completed=False,
        end_time__isnull=True
    ).first()

    # Get today's statistics
    today = timezone.now().date()
    today_sessions = FocusSession.objects.filter(
        user=request.user,
        start_time__date=today,
        completed=True
    )
    daily_minutes = sum(s.duration_minutes or 0 for s in today_sessions)

    # Check for overload
    overload_status = check_overload_alert(request.user)

    context = {
        'focus_models': focus_models,
        'preference': preference,
        'active_session': active_session,
        'daily_minutes': daily_minutes,
        'overload_status': overload_status,
    }

    return render(request, 'focus_break/timer.html', context)

@login_required
def start_focus_session(request):
    """Start a new focus session"""
    if request.method == 'POST':
        model_id = request.POST.get('focus_model')

        if model_id:
            focus_model = get_object_or_404(FocusModel, id=model_id)
        else:
            # Use default from preference
            preference = UserPreference.objects.get(user=request.user)
            focus_model = preference.default_focus_model

        # Check if there's already an active session
        active_session = FocusSession.objects.filter(
            user=request.user,
            completed=False,
            end_time__isnull=True
        ).first()

        if active_session:
            messages.warning(request, 'You already have an active focus session.')
            return redirect('focus_timer')

        # Create new focus session
        session = FocusSession.objects.create(
            user=request.user,
            focus_model=focus_model,
            start_time=timezone.now()
        )

        messages.success(request, f'Focus session started! Stay focused for {focus_model.focus_duration} minutes.')
        return redirect('focus_timer')

    return redirect('focus_timer')

@login_required
def end_focus_session(request, pk):
    """End a focus session"""
    session = get_object_or_404(FocusSession, pk=pk, user=request.user)

    if not session.end_time:
        session.end_time = timezone.now()
        session.duration_minutes = session.calculate_duration()
        session.completed = True
        session.save()

        # Get break recommendation
        consecutive = get_consecutive_sessions(request.user)
        today = timezone.now().date()
        daily_minutes = sum(
            s.duration_minutes or 0 for s in FocusSession.objects.filter(
                user=request.user,
                start_time__date=today,
                completed=True
            )
        )

        break_rec = get_break_recommendation(request.user, consecutive, daily_minutes)

        messages.success(
            request,
            f'Focus session completed! {break_rec["message"]} Recommended break: {break_rec["break_duration"]} minutes.'
        )
    else:
        messages.warning(request, 'This session has already ended.')

    return redirect('focus_timer')

@login_required
def start_break(request):
    """Start a break session"""
    if request.method == 'POST':
        duration = int(request.POST.get('duration', 5))

        # Get last focus session
        last_focus = FocusSession.objects.filter(
            user=request.user,
            completed=True
        ).order_by('-end_time').first()

        BreakSession.objects.create(
            user=request.user,
            focus_session=last_focus,
            start_time=timezone.now(),
            recommended_duration=duration
        )

        messages.success(request, f'Break started! Relax for {duration} minutes.')
        return redirect('focus_timer')

    return redirect('focus_timer')

@login_required
def end_break(request, pk):
    """End a break session"""
    break_session = get_object_or_404(BreakSession, pk=pk, user=request.user)

    if not break_session.end_time:
        break_session.end_time = timezone.now()
        delta = break_session.end_time - break_session.start_time
        break_session.actual_duration = int(delta.total_seconds() / 60)
        break_session.completed = True
        break_session.save()

        messages.success(request, 'Break completed! Ready to focus again?')
    else:
        messages.warning(request, 'This break has already ended.')

    return redirect('focus_timer')

@login_required
def preferences_view(request):
    """View and update focus/break preferences"""
    preference, created = UserPreference.objects.get_or_create(user=request.user)
    focus_models = FocusModel.objects.all()

    if request.method == 'POST':
        model_id = request.POST.get('default_focus_model')
        daily_limit = request.POST.get('daily_study_limit')
        enable_alerts = request.POST.get('enable_overload_alerts') == 'on'

        if model_id:
            preference.default_focus_model = get_object_or_404(FocusModel, id=model_id)
        if daily_limit:
            preference.daily_study_limit = int(daily_limit)
        preference.enable_overload_alerts = enable_alerts
        preference.save()

        messages.success(request, 'Preferences updated successfully!')
        return redirect('preferences')

    context = {
        'preference': preference,
        'focus_models': focus_models,
    }

    return render(request, 'focus_break/preferences.html', context)
