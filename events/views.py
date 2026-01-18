from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Event
from .forms import EventForm
from study_sessions.models import StudySession
from ai.event_integration import generate_ai_study_sessions

@login_required
def event_list(request):
    events = Event.objects.filter(user=request.user)
    upcoming_events = events.filter(event_date__gte=timezone.now()).order_by('event_date')
    past_events = events.filter(event_date__lt=timezone.now()).order_by('-event_date')

    return render(request, 'events/event_list.html', {
        'upcoming_events': upcoming_events,
        'past_events': past_events
    })

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    study_sessions = event.study_sessions.all()

    # Phase 3: Check for diagnostic test
    from diagnostics.models import DiagnosticTest
    try:
        diagnostic_test = DiagnosticTest.objects.get(event=event, user=request.user)
    except DiagnosticTest.DoesNotExist:
        diagnostic_test = None

    context = {
        'event': event,
        'study_sessions': study_sessions,
        'completion': event.completion_percentage(),
        'days_remaining': event.days_until_event(),
        'at_risk': event.is_at_risk(),
        'diagnostic_test': diagnostic_test,
    }

    return render(request, 'events/event_detail.html', context)

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()

            # Generate study sessions automatically
            generate_study_sessions(event)

            # Phase 3: Create diagnostic test if file uploaded
            diagnostic_file = form.cleaned_data.get('diagnostic_file')
            if diagnostic_file:
                from diagnostics.models import DiagnosticTest
                diagnostic_test = DiagnosticTest.objects.create(
                    user=request.user,
                    event=event,
                    title=f"Diagnostic Test - {event.title}",
                    uploaded_file=diagnostic_file
                )
                messages.success(request,
                    f'Event "{event.title}" created with study sessions and diagnostic test uploaded! '
                    f'Add questions to your diagnostic test to analyze it.'
                )
            else:
                messages.success(request, f'Event "{event.title}" created successfully with auto-generated study sessions!')

            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {'form': form, 'action': 'Create'})

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            updated_event = form.save()

            # Regenerate study sessions if prep time or date changed
            event.study_sessions.filter(status='pending').delete()
            generate_study_sessions(updated_event)

            messages.success(request, f'Event "{updated_event.title}" updated successfully!')
            return redirect('event_detail', pk=updated_event.pk)
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event_form.html', {'form': form, 'action': 'Update'})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)
    if request.method == 'POST':
        event_title = event.title
        event.delete()
        messages.success(request, f'Event "{event_title}" deleted successfully!')
        return redirect('event_list')

    return render(request, 'events/event_confirm_delete.html', {'event': event})

def generate_study_sessions(event):
    """
    Generate study sessions using AI or fallback to deterministic method.

    This function tries to use AI to generate intelligent study sessions.
    If AI fails or is disabled, it falls back to the deterministic method.
    """
    # Try AI-powered session generation first
    ai_sessions = generate_ai_study_sessions(event, force_regenerate=True)

    if ai_sessions and len(ai_sessions) > 0:
        # AI successfully generated sessions
        return ai_sessions

    # Fallback to deterministic method if AI fails or is disabled
    return _generate_deterministic_sessions(event)


def _generate_deterministic_sessions(event):
    """
    Fallback: Generate study sessions using deterministic logic.

    This is the original method used when AI is unavailable.
    """
    # Calculate days until event
    days_until = (event.event_date.date() - timezone.now().date()).days

    # If event is in the past or today, create sessions for future dates anyway
    # This ensures study sessions are always created
    if days_until <= 0:
        days_until = 7  # Default to 7 days for planning

    # Convert prep time from hours to minutes
    total_prep_minutes = int(event.estimated_prep_time * 60)

    # Determine optimal session duration (between 25-60 minutes)
    if total_prep_minutes <= 120:  # 2 hours or less
        session_duration = 25
    elif total_prep_minutes <= 300:  # 5 hours or less
        session_duration = 45
    else:
        session_duration = 60

    # Calculate number of sessions needed
    num_sessions = max(1, int(total_prep_minutes / session_duration))

    # Distribute sessions across available days
    sessions_per_day = max(1, num_sessions // max(1, days_until))

    current_date = timezone.now().date()
    session_count = 0
    default_start_time = timezone.datetime.strptime('18:00', '%H:%M').time()

    sessions = []

    for day in range(days_until):
        if session_count >= num_sessions:
            break

        session_date = current_date + timedelta(days=day)

        for session_num in range(sessions_per_day):
            if session_count >= num_sessions:
                break

            # Calculate start time (stagger sessions if multiple per day)
            hour_offset = session_num * 2
            start_time = (
                timezone.datetime.combine(timezone.datetime.today(), default_start_time) +
                timedelta(hours=hour_offset)
            ).time()

            session = StudySession.objects.create(
                event=event,
                date=session_date,
                start_time=start_time,
                duration_minutes=session_duration,
                suggested_content=f"Study session {session_count + 1} of {num_sessions}",
                status='pending'
            )

            sessions.append(session)
            session_count += 1

    return sessions
