from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import FocusSession, BreakSession, FocusModel, UserPreference
from .utils import get_break_recommendation, check_overload_alert, get_consecutive_sessions
from study_sessions.models import StudySession

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

    # Calculate hours correctly
    daily_hours = daily_minutes / 60.0

    # Check for overload
    overload_status = check_overload_alert(request.user)

    context = {
        'focus_models': focus_models,
        'preference': preference,
        'active_session': active_session,
        'daily_minutes': daily_minutes,
        'daily_hours': daily_hours,
        'overload_status': overload_status,
    }

    return render(request, 'focus_break/timer.html', context)

@login_required
def start_focus_session(request):
    """Start a new focus session"""
    if request.method == 'POST':
        model_id = request.POST.get('focus_model')
        study_session_id = request.POST.get('study_session_id')

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

        # Link to study session if provided
        study_session = None
        if study_session_id:
            try:
                study_session = StudySession.objects.get(
                    id=study_session_id,
                    event__user=request.user
                )
                # Update study session status
                if not study_session.actual_start_time:
                    study_session.actual_start_time = timezone.now()
                    study_session.status = 'in_progress'
                    study_session.save()
            except StudySession.DoesNotExist:
                pass

        # Create new focus session
        session = FocusSession.objects.create(
            user=request.user,
            focus_model=focus_model,
            study_session=study_session,
            start_time=timezone.now()
        )

        if study_session:
            messages.success(
                request,
                f'Focus session started for "{study_session.event.title}"! '
                f'Stay focused for {focus_model.focus_duration} minutes.'
            )
        else:
            messages.success(
                request,
                f'Focus session started! Stay focused for {focus_model.focus_duration} minutes.'
            )
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

        # Update linked study session if exists
        if session.study_session:
            study_session = session.study_session

            # Calculate total focus time from all linked focus sessions
            total_focus_minutes = sum(
                fs.duration_minutes or 0
                for fs in study_session.focus_sessions.filter(completed=True)
            )

            # Update actual duration
            study_session.actual_duration_minutes = total_focus_minutes
            study_session.actual_end_time = timezone.now()

            # Auto-complete if total time meets or exceeds target
            if total_focus_minutes >= study_session.duration_minutes:
                study_session.status = 'completed'
                messages.info(
                    request,
                    f'Study session "{study_session.event.title}" completed! '
                    f'Total time: {total_focus_minutes}/{study_session.duration_minutes} minutes.'
                )
            else:
                # Keep in progress if more time needed
                study_session.status = 'in_progress'
                remaining = study_session.duration_minutes - total_focus_minutes
                messages.info(
                    request,
                    f'Progress: {total_focus_minutes}/{study_session.duration_minutes} minutes. '
                    f'{remaining} minutes remaining.'
                )

            study_session.save()

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
