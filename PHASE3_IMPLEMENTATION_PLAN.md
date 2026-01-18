# Phase 3 Implementation Plan - AI-Enhanced Learning Orchestration

**Date:** 2026-01-16
**Status:** Planning Complete, Ready for Implementation

---

## 🎯 Overview

Phase 3 adds intelligent learning orchestration based on:
- Emotional state tracking (energy, stress, focus)
- Diagnostic test analysis
- AI-driven plan adjustments
- Behavior-based insights

**Core Principle:** AI suggests, User decides (No automatic changes)

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Phase 3 Architecture                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   │
│  │  Emotional   │   │  Diagnostic  │   │     Plan     │   │
│  │    State     │   │    Tests     │   │  Adjustment  │   │
│  │  Collection  │   │   Analysis   │   │  Suggestions │   │
│  └──────────────┘   └──────────────┘   └──────────────┘   │
│         │                   │                   │           │
│         └───────────────────┴───────────────────┘           │
│                             │                               │
│                    ┌────────▼────────┐                     │
│                    │   AI Services   │                     │
│                    │   (ai/services) │                     │
│                    └────────┬────────┘                     │
│                             │                               │
│         ┌───────────────────┼───────────────────┐          │
│         │                   │                   │          │
│  ┌──────▼──────┐   ┌────────▼────────┐  ┌──────▼──────┐  │
│  │   Events    │   │ Study Sessions  │  │  Focus      │  │
│  │  (existing) │   │   (existing)    │  │  Sessions   │  │
│  └─────────────┘   └─────────────────┘  │  (existing) │  │
│                                          └─────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗂️ New Models to Create

### 1. EmotionalStateLog

**App:** `emotional_state/` (new Django app)

**Model:**
```python
class EmotionalStateLog(models.Model):
    SOURCE_CHOICES = [
        ('self_report', 'Self-Reported'),
        ('inferred', 'Inferred from Behavior'),
    ]

    LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Emotional dimensions (STRICT - only these 3)
    energy_level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    stress_level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    focus_level = models.CharField(max_length=10, choices=LEVEL_CHOICES)

    # Metadata
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    trigger_context = models.CharField(max_length=100, blank=True)  # e.g., "session_end", "day_start"

    # Optional: Link to study session if triggered by session end
    study_session = models.ForeignKey('study_sessions.StudySession',
                                     on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='emotional_logs')

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
        ]
```

### 2. DiagnosticTest

**App:** `diagnostics/` (new Django app)

**Models:**
```python
class DiagnosticTest(models.Model):
    event = models.OneToOneField('events.Event', on_delete=models.CASCADE, related_name='diagnostic_test')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    uploaded_file = models.FileField(upload_to='diagnostics/', blank=True, null=True)

    # Analysis results (JSON)
    analysis_result = models.JSONField(blank=True, null=True)
    analyzed_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class DiagnosticQuestion(models.Model):
    ERROR_TYPE_CHOICES = [
        ('conceptual', 'Conceptual Error'),
        ('application', 'Application Error'),
        ('reasoning', 'Reasoning Error'),
    ]

    diagnostic_test = models.ForeignKey(DiagnosticTest, on_delete=models.CASCADE, related_name='questions')

    question_number = models.IntegerField()
    question_text = models.TextField()
    correct_answer = models.TextField()
    user_answer = models.TextField()
    topic = models.CharField(max_length=200, blank=True)

    # Analysis fields
    is_correct = models.BooleanField(default=False)
    error_type = models.CharField(max_length=20, choices=ERROR_TYPE_CHOICES, blank=True)

    class Meta:
        ordering = ['question_number']
        unique_together = ['diagnostic_test', 'question_number']
```

### 3. PlanAdjustmentSuggestion

**App:** `diagnostics/` (reuse)

**Model:**
```python
class PlanAdjustmentSuggestion(models.Model):
    ADJUSTMENT_TYPE_CHOICES = [
        ('split', 'Split Task'),
        ('shorten', 'Shorten Duration'),
        ('reorder', 'Reorder Tasks'),
        ('focus_mode_change', 'Change Focus Mode'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='adjustment_suggestions')

    # Trigger context
    triggered_by = models.CharField(max_length=100)  # e.g., "high_stress", "at_risk", "overrun"
    triggered_at = models.DateTimeField(auto_now_add=True)

    # AI suggestion data (JSON)
    context = models.JSONField()  # Stores emotional state, error topics, etc.
    adjustments = models.JSONField()  # List of suggested adjustments
    rationale = models.TextField()  # AI's explanation

    # User decision
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_at = models.DateTimeField(blank=True, null=True)
    user_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-triggered_at']
```

---

## 🧠 AI Services to Implement

### 1. Diagnostic Analysis Service

**Location:** `ai/services/diagnostic_analyzer.py`

**Function:**
```python
def analyze_diagnostic_test(diagnostic_test: DiagnosticTest) -> dict:
    """
    Analyze diagnostic test errors and group them.

    Returns:
    {
        "error_groups": [
            {
                "topic": "Algebra",
                "error_type": "conceptual",
                "error_count": 3
            },
            ...
        ]
    }
    """
```

**AI Prompt Template:** `ai/prompts/diagnostic_analysis.txt`

### 2. Plan Adjustment Service

**Location:** `ai/services/plan_adjuster.py`

**Function:**
```python
def suggest_plan_adjustments(
    user: User,
    event: Event,
    trigger_reason: str,
    emotional_state: dict,
    diagnostic_errors: dict
) -> dict:
    """
    Generate plan adjustment suggestions based on context.

    Returns:
    {
        "context": {...},
        "adjustments": [...],
        "rationale": "..."
    }
    """
```

**AI Prompt Template:** `ai/prompts/plan_adjustment.txt`

### 3. Session Generator from Diagnostics

**Location:** `ai/services/diagnostic_session_generator.py`

**Function:**
```python
def generate_review_sessions(
    event: Event,
    error_groups: list
) -> list[StudySession]:
    """
    Create targeted review sessions from error analysis.

    Each session:
    - Targets one error group
    - Duration: 25-60 minutes
    - Type: concept_review | practice | revision
    """
```

---

## 📝 AI Schemas

**Location:** `ai/schemas.py` (extend existing)

```python
# Diagnostic Analysis Schema
class DiagnosticErrorGroup(TypedDict):
    topic: str
    error_type: Literal['conceptual', 'application', 'reasoning']
    error_count: int

class DiagnosticAnalysisResult(TypedDict):
    error_groups: List[DiagnosticErrorGroup]


# Plan Adjustment Schema
class EmotionalContext(TypedDict):
    energy: Literal['low', 'medium', 'high']
    stress: Literal['low', 'medium', 'high']
    focus: Literal['low', 'medium', 'high']

class PlanAdjustment(TypedDict):
    type: Literal['split', 'shorten', 'reorder', 'focus_mode_change']
    target: str  # task_id or task_title
    new_duration_minutes: Optional[int]
    new_order: Optional[int]
    new_focus_mode: Optional[str]

class PlanAdjustmentResult(TypedDict):
    context: dict  # Contains emotional_state, dominant_error_topic, etc.
    adjustments: List[PlanAdjustment]
    rationale: str
```

---

## 🖥️ Views & URLs

### Emotional State Collection

**URLs:**
- `/emotional/log/` - POST endpoint to log state
- `/emotional/prompt/` - GET prompt for state collection

**Views:**
- `log_emotional_state(request)` - Save self-reported state
- `prompt_emotional_state(request)` - Show collection form

**Triggers:**
- Start of day (user visits dashboard)
- End of study session (redirect after session completion)

### Diagnostic Tests

**URLs:**
- `/diagnostics/upload/<event_id>/` - Upload diagnostic test
- `/diagnostics/<test_id>/` - View test details
- `/diagnostics/<test_id>/analyze/` - Trigger AI analysis
- `/diagnostics/<test_id>/add-question/` - Add question manually

**Views:**
- `upload_diagnostic_test(request, event_id)`
- `view_diagnostic_test(request, test_id)`
- `analyze_diagnostic_test(request, test_id)`
- `add_diagnostic_question(request, test_id)`

### Plan Adjustments

**URLs:**
- `/adjustments/` - List all pending suggestions
- `/adjustments/<suggestion_id>/` - View suggestion detail
- `/adjustments/<suggestion_id>/accept/` - Accept suggestion
- `/adjustments/<suggestion_id>/reject/` - Reject suggestion

**Views:**
- `list_adjustment_suggestions(request)`
- `view_adjustment_suggestion(request, suggestion_id)`
- `accept_adjustment(request, suggestion_id)`
- `reject_adjustment(request, suggestion_id)`

---

## 🎨 Templates

### 1. Emotional State Collection
- `emotional_state/prompt.html` - Simple 3-slider form
- `emotional_state/thank_you.html` - Confirmation message

### 2. Diagnostic Tests
- `diagnostics/upload.html` - File upload form
- `diagnostics/detail.html` - Test details with questions
- `diagnostics/add_question.html` - Manual question entry
- `diagnostics/analysis_result.html` - Error groups visualization

### 3. Plan Adjustments
- `adjustments/list.html` - List of pending suggestions
- `adjustments/detail.html` - Suggestion with rationale & options
- `adjustments/accepted.html` - Confirmation

---

## 🔄 Behavioral Inference Logic

**Location:** `emotional_state/utils.py`

**Functions:**

```python
def infer_low_energy(user: User, session: StudySession) -> bool:
    """Check if session ended early (< 50% of planned duration)"""

def infer_high_stress(user: User) -> bool:
    """Check for repeated postponements in last 7 days"""

def infer_low_focus(user: User) -> bool:
    """Check for repeated time overruns"""

def auto_log_inferred_state(user: User, trigger: str):
    """Create inferred emotional log"""
```

---

## 🧪 Testing Strategy

### Unit Tests
- `test_emotional_state_model.py`
- `test_diagnostic_analysis.py`
- `test_plan_adjustment.py`
- `test_behavioral_inference.py`

### Integration Tests
- `test_diagnostic_to_sessions.py` - Full flow from upload to sessions
- `test_adjustment_flow.py` - Trigger → AI → User decision

### E2E Tests
- `test_phase3_full_workflow.py` - Complete user journey

---

## 📦 Dependencies

**New Python packages:**
```txt
PyPDF2>=3.0.0           # For PDF parsing
python-magic>=0.4.27    # For file type detection
```

**Existing packages (already have):**
- anthropic / openai (AI providers)
- django (web framework)

---

## 🚀 Implementation Order

### Sprint 1: Data Models (Days 1-2)
1. Create `emotional_state` app
2. Create `diagnostics` app
3. Implement models
4. Run migrations
5. Add admin interfaces

### Sprint 2: AI Services (Days 3-4)
1. Create AI prompts
2. Implement diagnostic analyzer
3. Implement plan adjuster
4. Implement session generator
5. Add unit tests

### Sprint 3: Views & Templates (Days 5-6)
1. Emotional state collection views
2. Diagnostic upload & management views
3. Plan adjustment views
4. Create all templates
5. Add URL routing

### Sprint 4: Integration & Testing (Days 7-8)
1. Behavioral inference logic
2. Integration between components
3. E2E testing
4. Bug fixes
5. Documentation

---

## ⚠️ Important Constraints

### DO ✅
- Keep AI logic in `ai/` folder only
- Require user confirmation for all AI suggestions
- Provide clear rationale for all AI outputs
- Use only the 3 approved emotional dimensions
- Make all AI processes visible and explainable

### DON'T ❌
- Add AI calls to models, signals, or migrations
- Make automatic changes to user's plan
- Use psychological labels ("weak student", etc.)
- Add features not in requirements
- Store free-text emotional data

---

## 📊 Success Criteria

✅ Can collect emotional state (self-reported + inferred)
✅ Can upload & analyze diagnostic tests
✅ Can generate targeted review sessions from errors
✅ Can suggest plan adjustments with rationale
✅ All AI suggestions require user confirmation
✅ No automatic modifications to schedules
✅ All code in appropriate layers (AI in `ai/`)
✅ Complete test coverage
✅ Documentation updated

---

## 🔐 Privacy & Ethics

- Emotional data is minimal (3 dimensions only)
- No psychological profiling
- No comparison between users
- No medical claims
- Data used only for schedule optimization
- User controls all decisions
- Clear explanation of all inferences

---

**Ready to implement!** 🚀

This plan follows all requirements strictly and maintains clear separation of concerns.
