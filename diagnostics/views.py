"""
Views for diagnostics app - handles diagnostic tests and plan adjustments.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from django.db import transaction

from events.models import Event
from .models import DiagnosticTest, DiagnosticQuestion, PlanAdjustmentSuggestion


# ==================== Diagnostic Test Views ====================

@login_required
@require_http_methods(["GET", "POST"])
def upload_diagnostic_test(request, event_id):
    """
    Upload a diagnostic test for an event.
    Supports PDF upload or manual entry.
    """
    event = get_object_or_404(Event, id=event_id, user=request.user)

    # Check if test already exists for this event
    existing_test = DiagnosticTest.objects.filter(event=event).first()
    if existing_test:
        messages.info(request, f"A diagnostic test already exists for this event. You can add more questions.")
        return redirect('diagnostic_detail', test_id=existing_test.id)

    if request.method == 'POST':
        title = request.POST.get('title', f"Diagnostic Test - {event.title}")
        uploaded_file = request.FILES.get('pdf_file')

        # Create diagnostic test
        test = DiagnosticTest.objects.create(
            user=request.user,
            event=event,
            title=title,
            uploaded_file=uploaded_file
        )

        messages.success(request, f"Diagnostic test created! Now add questions to it.")
        return redirect('diagnostic_add_question', test_id=test.id)

    context = {
        'event': event,
    }
    return render(request, 'diagnostics/upload.html', context)


@login_required
@require_http_methods(["GET"])
def view_diagnostic_test(request, test_id):
    """
    View diagnostic test details with all questions and score.
    """
    test = get_object_or_404(DiagnosticTest, id=test_id, user=request.user)
    questions = test.questions.all().order_by('question_number')

    # Group incorrect questions by topic
    incorrect_questions = questions.filter(is_correct=False)
    error_groups = {}
    for q in incorrect_questions:
        topic = q.topic or 'Uncategorized'
        if topic not in error_groups:
            error_groups[topic] = []
        error_groups[topic].append(q)

    context = {
        'test': test,
        'questions': questions,
        'error_groups': error_groups,
    }
    return render(request, 'diagnostics/detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def add_diagnostic_question(request, test_id):
    """
    Add a question to a diagnostic test (manual entry).
    """
    test = get_object_or_404(DiagnosticTest, id=test_id, user=request.user)

    if request.method == 'POST':
        question_number = int(request.POST.get('question_number', test.questions.count() + 1))
        question_text = request.POST.get('question_text')
        correct_answer = request.POST.get('correct_answer')
        user_answer = request.POST.get('user_answer')
        topic = request.POST.get('topic', '')
        error_type = request.POST.get('error_type', '')

        # Validate required fields
        if not all([question_text, correct_answer, user_answer]):
            messages.error(request, "Please fill in all required fields.")
            return redirect('diagnostic_add_question', test_id=test_id)

        # Create question
        DiagnosticQuestion.objects.create(
            diagnostic_test=test,
            question_number=question_number,
            question_text=question_text,
            correct_answer=correct_answer,
            user_answer=user_answer,
            topic=topic,
            error_type=error_type
        )

        # Check if user wants to add more
        if 'add_another' in request.POST:
            messages.success(request, f"Question {question_number} added! Add another one.")
            return redirect('diagnostic_add_question', test_id=test_id)
        else:
            messages.success(request, f"Question {question_number} added! View your test.")
            return redirect('diagnostic_detail', test_id=test_id)

    # GET request - show form
    next_question_number = test.questions.count() + 1
    context = {
        'test': test,
        'next_question_number': next_question_number,
        'error_types': DiagnosticQuestion.ERROR_TYPE_CHOICES,
    }
    return render(request, 'diagnostics/add_question.html', context)


@login_required
@require_http_methods(["POST"])
def analyze_diagnostic_test(request, test_id):
    """
    Trigger AI analysis of diagnostic test.
    This will call AI service to analyze error patterns.
    """
    test = get_object_or_404(DiagnosticTest, id=test_id, user=request.user)

    # Check if test has questions
    if test.total_questions == 0:
        messages.error(request, "Cannot analyze test with no questions. Add questions first.")
        return redirect('diagnostic_detail', test_id=test_id)

    # TODO: Call AI service for analysis
    # For now, create a simple analysis
    incorrect_questions = test.questions.filter(is_correct=False)

    # Group errors by topic
    topic_errors = {}
    for q in incorrect_questions:
        topic = q.topic or 'Uncategorized'
        topic_errors[topic] = topic_errors.get(topic, 0) + 1

    # Find dominant error topic
    dominant_topic = max(topic_errors.items(), key=lambda x: x[1])[0] if topic_errors else None

    # Save basic analysis result
    test.analysis_result = {
        'total_questions': test.total_questions,
        'correct': test.correct_count,
        'incorrect': test.incorrect_count,
        'score_percentage': test.score_percentage,
        'error_groups': [
            {
                'topic': topic,
                'error_count': count,
                'percentage': int((count / test.incorrect_count) * 100) if test.incorrect_count > 0 else 0
            }
            for topic, count in topic_errors.items()
        ],
        'dominant_error_topic': dominant_topic,
        'analyzed_at': timezone.now().isoformat()
    }
    test.analyzed_at = timezone.now()
    test.save()

    messages.success(request, "Test analyzed successfully! Check the results below.")

    # TODO: Optionally trigger plan adjustment suggestion here

    return redirect('diagnostic_detail', test_id=test_id)


# ==================== Plan Adjustment Suggestion Views ====================

@login_required
@require_http_methods(["GET"])
def list_adjustment_suggestions(request):
    """
    List all plan adjustment suggestions for the user.
    Filter by status (pending/accepted/rejected).
    """
    status_filter = request.GET.get('status', 'pending')

    if status_filter == 'all':
        suggestions = PlanAdjustmentSuggestion.objects.filter(user=request.user)
    else:
        suggestions = PlanAdjustmentSuggestion.objects.filter(
            user=request.user,
            status=status_filter
        )

    suggestions = suggestions.order_by('-triggered_at')

    context = {
        'suggestions': suggestions,
        'status_filter': status_filter,
    }
    return render(request, 'diagnostics/suggestions_list.html', context)


@login_required
@require_http_methods(["GET"])
def view_adjustment_suggestion(request, suggestion_id):
    """
    View details of a plan adjustment suggestion.
    Shows context, adjustments, and rationale.
    """
    suggestion = get_object_or_404(PlanAdjustmentSuggestion, id=suggestion_id, user=request.user)

    context = {
        'suggestion': suggestion,
    }
    return render(request, 'diagnostics/suggestion_detail.html', context)


@login_required
@require_http_methods(["POST"])
def accept_adjustment(request, suggestion_id):
    """
    Accept a plan adjustment suggestion.
    """
    suggestion = get_object_or_404(PlanAdjustmentSuggestion, id=suggestion_id, user=request.user)

    if suggestion.status != 'pending':
        messages.warning(request, "This suggestion has already been reviewed.")
        return redirect('adjustment_suggestion_detail', suggestion_id=suggestion_id)

    user_notes = request.POST.get('notes', '')

    with transaction.atomic():
        suggestion.accept(user_notes=user_notes)

        # TODO: Apply the adjustments to study sessions
        # This should be done by calling a service that:
        # 1. Parses the adjustments
        # 2. Modifies the relevant study sessions
        # 3. Logs the changes

        messages.success(request, "Plan adjustment accepted! Your study sessions will be updated accordingly.")

    return redirect('adjustment_suggestions_list')


@login_required
@require_http_methods(["POST"])
def reject_adjustment(request, suggestion_id):
    """
    Reject a plan adjustment suggestion.
    """
    suggestion = get_object_or_404(PlanAdjustmentSuggestion, id=suggestion_id, user=request.user)

    if suggestion.status != 'pending':
        messages.warning(request, "This suggestion has already been reviewed.")
        return redirect('adjustment_suggestion_detail', suggestion_id=suggestion_id)

    user_notes = request.POST.get('notes', '')

    suggestion.reject(user_notes=user_notes)

    messages.info(request, "Plan adjustment rejected. Your current plan remains unchanged.")

    return redirect('adjustment_suggestions_list')
