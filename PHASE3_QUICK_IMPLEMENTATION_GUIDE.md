# Phase 3 - Quick Implementation Guide

**Status:** Models Created, Ready for Rapid Implementation
**Date:** 2026-01-16

---

## ✅ Completed (in this session)

1. ✅ Created `PHASE3_IMPLEMENTATION_PLAN.md` - Full architectural design
2. ✅ Created `emotional_state` Django app
3. ✅ Created `diagnostics` Django app
4. ✅ Implemented `EmotionalStateLog` model with all methods
5. ✅ Implemented `DiagnosticTest`, `DiagnosticQuestion`, `PlanAdjustmentSuggestion` models
6. ✅ Added apps to `INSTALLED_APPS` in settings.py

---

## 🚀 Next Steps to Complete Phase 3

### Step 1: Create Migrations (2 minutes)
```bash
python manage.py makemigrations emotional_state
python manage.py makemigrations diagnostics
python manage.py migrate
```

### Step 2: Add Admin Interfaces (5 minutes)

Create `emotional_state/admin.py`:
```python
from django.contrib import admin
from .models import EmotionalStateLog

@admin.register(EmotionalStateLog)
class EmotionalStateLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'timestamp', 'energy_level', 'stress_level', 'focus_level', 'source']
    list_filter = ['source', 'energy_level', 'stress_level', 'focus_level', 'timestamp']
    search_fields = ['user__username']
    date_hierarchy = 'timestamp'
```

Create `diagnostics/admin.py`:
```python
from django.contrib import admin
from .models import DiagnosticTest, DiagnosticQuestion, PlanAdjustmentSuggestion

@admin.register(DiagnosticTest)
class DiagnosticTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'event', 'total_questions', 'score_percentage', 'is_analyzed']
    list_filter = ['analyzed_at', 'created_at']
    search_fields = ['title', 'user__username']

@admin.register(DiagnosticQuestion)
class DiagnosticQuestionAdmin(admin.ModelAdmin):
    list_display = ['diagnostic_test', 'question_number', 'topic', 'is_correct', 'error_type']
    list_filter = ['is_correct', 'error_type']

@admin.register(PlanAdjustmentSuggestion)
class PlanAdjustmentSuggestionAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'triggered_by', 'status', 'triggered_at']
    list_filter = ['status', 'triggered_by', 'triggered_at']
    search_fields = ['user__username', 'event__title']
```

### Step 3: Update Requirements (1 minute)

Add to `requirements.txt`:
```txt
PyPDF2>=3.0.0              # For PDF parsing
```

Install:
```bash
pip install PyPDF2>=3.0.0
```

### Step 4: Create AI Schemas (10 minutes)

Extend `ai/schemas.py`:
```python
# Add these to existing schemas.py

from typing import TypedDict, List, Literal, Optional

# Diagnostic Analysis Schemas
class DiagnosticErrorGroup(TypedDict):
    topic: str
    error_type: Literal['conceptual', 'application', 'reasoning']
    error_count: int

class DiagnosticAnalysisResult(TypedDict):
    error_groups: List[DiagnosticErrorGroup]

# Plan Adjustment Schemas
class EmotionalContext(TypedDict):
    energy: Literal['low', 'medium', 'high']
    stress: Literal['low', 'medium', 'high']
    focus: Literal['low', 'medium', 'high']

class PlanAdjustment(TypedDict):
    type: Literal['split', 'shorten', 'reorder', 'focus_mode_change']
    target: str
    new_duration_minutes: Optional[int]
    new_order: Optional[int]
    new_focus_mode: Optional[str]

class PlanAdjustmentResult(TypedDict):
    context: dict
    adjustments: List[PlanAdjustment]
    rationale: str
```

### Step 5: Create AI Prompts (15 minutes)

Create `ai/prompts/diagnostic_analysis.txt`:
```
You are analyzing a diagnostic test to identify error patterns.

Event: {event_title}
Subject: {subject}
Total Questions: {total_questions}
Incorrect Answers: {incorrect_count}

Questions with Incorrect Answers:
{incorrect_questions}

Task:
1. Group errors by topic
2. Classify each error as: conceptual, application, or reasoning
3. Count errors per group

STRICT RULES:
- Do NOT rate student ability
- Do NOT compare to others
- Do NOT use labels like "weak" or "strong"
- Only analyze error patterns

Output Format (JSON):
{
  "error_groups": [
    {
      "topic": "specific topic name",
      "error_type": "conceptual|application|reasoning",
      "error_count": number
    }
  ]
}
```

Create `ai/prompts/plan_adjustment.txt`:
```
You are suggesting study plan adjustments based on student context.

Event: {event_title}
Current Status:
- Days until event: {days_until}
- Completion: {completion_percent}%
- Sessions remaining: {sessions_remaining}

Trigger: {trigger_reason}

Current Emotional State:
- Energy: {energy}
- Stress: {stress}
- Focus: {focus}

Diagnostic Errors (if any):
{error_summary}

Task:
Suggest helpful adjustments to the study plan.

Available adjustment types:
- split: Break a long session into smaller parts
- shorten: Reduce session duration
- reorder: Change task sequence
- focus_mode_change: Suggest different focus technique

STRICT RULES:
- Provide clear rationale for EVERY suggestion
- Be specific about which tasks to adjust
- Consider both emotional state AND diagnostic errors
- Do NOT make automatic changes (user must approve)
- Suggestions should be actionable and practical

Output Format (JSON):
{
  "context": {
    "dominant_error_topic": "topic or null",
    "emotional_state": {
      "energy": "low|medium|high",
      "stress": "low|medium|high",
      "focus": "low|medium|high"
    }
  },
  "adjustments": [
    {
      "type": "split|shorten|reorder|focus_mode_change",
      "target": "task title or session ID",
      "new_duration_minutes": number (if applicable),
      "new_order": number (if reorder),
      "new_focus_mode": "mode name" (if focus_mode_change)
    }
  ],
  "rationale": "Clear explanation of why these adjustments help"
}
```

### Step 6: Create Behavioral Inference Utilities (20 minutes)

Create `emotional_state/utils.py`:
```python
"""
Behavioral inference utilities for emotional state detection.

Infers emotional states from user behavior patterns.
"""
from django.utils import timezone
from datetime import timedelta
from .models import EmotionalStateLog


def infer_low_energy(user, session=None):
    """
    Detect low energy from early session termination.

    Returns True if session ended < 50% of planned duration.
    """
    if not session:
        return False

    if not session.actual_end_time or not session.actual_start_time:
        return False

    actual_minutes = (session.actual_end_time - session.actual_start_time).total_seconds() / 60
    planned_minutes = session.duration_minutes

    return actual_minutes < (planned_minutes * 0.5)


def infer_high_stress(user):
    """
    Detect high stress from repeated postponements.

    Returns True if 3+ sessions postponed in last 7 days.
    """
    from study_sessions.models import StudySession

    week_ago = timezone.now() - timedelta(days=7)
    postponed_count = StudySession.objects.filter(
        event__user=user,
        status='postponed',
        updated_at__gte=week_ago
    ).count()

    return postponed_count >= 3


def infer_low_focus(user):
    """
    Detect low focus from repeated time overruns.

    Returns True if 3+ sessions exceeded planned duration in last 7 days.
    """
    from study_sessions.models import StudySession

    week_ago = timezone.now() - timedelta(days=7)
    completed_sessions = StudySession.objects.filter(
        event__user=user,
        status='completed',
        actual_end_time__isnull=False,
        updated_at__gte=week_ago
    )

    overrun_count = 0
    for session in completed_sessions:
        if session.actual_duration_minutes and session.duration_minutes:
            if session.actual_duration_minutes > session.duration_minutes * 1.2:  # 20% overrun
                overrun_count += 1

    return overrun_count >= 3


def auto_log_inferred_state(user, trigger, session=None):
    """
    Automatically create inferred emotional log based on behavior.

    Args:
        user: User instance
        trigger: What triggered this inference (e.g., 'early_termination', 'overrun')
        session: Optional study session that triggered this
    """
    # Determine levels based on trigger type
    if trigger == 'early_termination':
        energy = 'low'
        stress = 'medium'  # Could be due to stress or energy
        focus = 'low'
    elif trigger == 'repeated_postponement':
        energy = 'medium'
        stress = 'high'
        focus = 'low'
    elif trigger == 'repeated_overrun':
        energy = 'medium'
        stress = 'medium'
        focus = 'low'
    else:
        # Default moderate levels for unknown triggers
        energy = 'medium'
        stress = 'medium'
        focus = 'medium'

    # Create log
    log = EmotionalStateLog.objects.create(
        user=user,
        energy_level=energy,
        stress_level=stress,
        focus_level=focus,
        source='inferred',
        trigger_context=trigger,
        study_session=session
    )

    return log


def should_prompt_emotional_check(user):
    """
    Determine if user should be prompted for emotional state.

    Prompts once per day max, or after significant events.
    """
    # Check if already logged today
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_logs = EmotionalStateLog.objects.filter(
        user=user,
        timestamp__gte=today_start,
        source='self_report'
    )

    return not today_logs.exists()
```

### Step 7: Create AI Services (40 minutes)

See separate implementation files (too long for this doc):
- `ai/services/diagnostic_analyzer.py`
- `ai/services/plan_adjuster.py`
- `ai/services/diagnostic_session_generator.py`

### Step 8: Create Views (60 minutes)

Create in respective apps:
- `emotional_state/views.py` - Log & prompt emotional state
- `diagnostics/views.py` - Upload, analyze, manage tests
- `diagnostics/adjustment_views.py` - View, accept, reject suggestions

### Step 9: Create URLs (10 minutes)

Create URL patterns for all new views.

### Step 10: Create Templates (90 minutes)

Create all HTML templates for forms and displays.

### Step 11: Testing (60 minutes)

Create comprehensive test scripts.

---

## 📊 Estimated Total Time

- **Already Done:** ~60 minutes (models, planning)
- **Remaining:** ~5-6 hours for full implementation
- **Total:** ~6-7 hours for complete Phase 3

---

## 🎯 Priority Order if Time Limited

If you need to prioritize:

1. **HIGH PRIORITY** (Core functionality):
   - Migrations
   - Admin interfaces
   - Emotional state collection (basic)
   - Diagnostic upload & manual entry

2. **MEDIUM PRIORITY** (AI features):
   - Diagnostic analysis service
   - Plan adjustment service
   - Behavioral inference

3. **LOW PRIORITY** (Polish):
   - Advanced templates
   - PDF parsing
   - Comprehensive testing

---

## 📝 Quick Command Reference

```bash
# Setup
python manage.py makemigrations
python manage.py migrate
pip install PyPDF2>=3.0.0

# Test
python manage.py shell
>>> from emotional_state.models import EmotionalStateLog
>>> from diagnostics.models import DiagnosticTest
>>> # Test model creation

# Run server
python manage.py runserver
```

---

**Phase 3 is architecturally complete!**
Models are ready, just need implementation of services, views, and templates.

All design decisions follow strict requirements:
- ✅ Minimal emotional data (only 3 dimensions)
- ✅ AI suggestions require user confirmation
- ✅ No automatic modifications
- ✅ Clear rationale for all AI outputs
- ✅ AI code isolated in ai/ folder
- ✅ Privacy-focused and ethical
