# AI Implementation Guide for EduFlow AI

This document explains how AI features have been implemented in EduFlow AI, how to configure them, and how to use them.

## 📋 Overview

EduFlow AI now includes three AI-powered features that follow a strict principle:

> **AI plans and advises. Deterministic logic executes and enforces. User always retains control.**

### Three AI Use Cases

1. **Event → Learning Plan Decomposition**: AI breaks down study goals into structured, actionable tasks
2. **Task-Level Time & Focus Suggestions**: AI recommends optimal durations and difficulty levels
3. **Adaptive Re-Planning**: AI detects patterns and suggests plan adjustments (triggered, not continuous)

## 🏗️ Architecture

### Module Structure

```
ai/
├── __init__.py                  # Module initialization
├── schemas.py                   # JSON validation schemas
├── services.py                  # AI API integration layer
├── event_integration.py         # Integration with Event/StudySession models
└── prompts/
    ├── plan_generation.txt      # Prompt template for learning plan generation
    └── replanning.txt           # Prompt template for adaptive re-planning
```

### Key Components

#### 1. **schemas.py** - Type Safety & Validation

Defines strict schemas for all AI outputs:

- `LearningTask`: Single study task with duration, difficulty, cognitive load
- `LearningPlan`: Complete learning plan with goal summary and task list
- `ReplanSuggestion`: Adaptive suggestions when issues detected

All schemas are validated before use to ensure AI output is predictable and safe.

#### 2. **services.py** - AI Service Layer

`AIService` class handles all AI interactions:

- **Provider abstraction**: Supports OpenAI, Anthropic, or mock responses
- **Caching**: Caches plans per event (24 hours) to reduce costs
- **Error handling**: Graceful fallback when AI fails
- **Logging**: All AI calls logged for debugging

#### 3. **event_integration.py** - Business Logic Integration

Helper functions that integrate AI into existing workflows:

- `generate_ai_study_sessions()`: Creates StudySession records from AI plan
- `check_for_replan_triggers()`: Detects when re-planning is needed
- `generate_replan_suggestions()`: Gets AI suggestions for plan adjustments

#### 4. **Prompt Templates**

Carefully engineered prompts that:

- Provide clear context about the learning goal
- Enforce output format (strict JSON)
- Include constraints (25-60 minute tasks, no dependencies)
- Give examples of good plans

## ⚙️ Configuration

### Step 1: Choose AI Provider

Edit `eduflow_ai/settings.py`:

```python
# AI Configuration
AI_ENABLED = True  # Enable AI features
AI_PROVIDER = 'openai'  # Options: 'mock', 'openai', 'anthropic'
AI_API_KEY = 'your-api-key-here'  # Your API key
AI_MODEL = 'gpt-4'  # Model to use
```

### Step 2: Provider-Specific Setup

#### Option A: OpenAI (GPT-4 / GPT-3.5)

1. Get API key from https://platform.openai.com/api-keys
2. Install package: `pip install openai`
3. Configure:

```python
AI_PROVIDER = 'openai'
AI_API_KEY = 'sk-...'  # Your OpenAI API key
AI_MODEL = 'gpt-4'  # or 'gpt-3.5-turbo' for lower cost
```

#### Option B: Anthropic (Claude)

1. Get API key from https://console.anthropic.com/
2. Install package: `pip install anthropic`
3. Configure:

```python
AI_PROVIDER = 'anthropic'
AI_API_KEY = 'sk-ant-...'  # Your Anthropic API key
AI_MODEL = 'claude-3-opus-20240229'  # or claude-3-sonnet for lower cost
```

#### Option C: Mock (Testing)

No API key needed, generates sample plans:

```python
AI_PROVIDER = 'mock'
AI_ENABLED = True  # Can test AI flow without costs
```

### Step 3: Environment Variables (Recommended for Production)

For security, use environment variables:

```python
import os

AI_ENABLED = os.environ.get('AI_ENABLED', 'False') == 'True'
AI_PROVIDER = os.environ.get('AI_PROVIDER', 'mock')
AI_API_KEY = os.environ.get('AI_API_KEY')
AI_MODEL = os.environ.get('AI_MODEL', 'gpt-4')
```

Then set in your environment:

```bash
# Windows
set AI_ENABLED=True
set AI_PROVIDER=openai
set AI_API_KEY=sk-...

# Linux/Mac
export AI_ENABLED=True
export AI_PROVIDER=openai
export AI_API_KEY=sk-...
```

## 🔌 Integration with Existing System

### Modifying Event Creation View

Update `events/views.py` to use AI when enabled:

```python
from ai.event_integration import generate_ai_study_sessions
from events.utils import generate_study_sessions  # Existing deterministic function

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()

            # Try AI-powered session generation
            ai_sessions = generate_ai_study_sessions(event)

            # Fall back to deterministic if AI fails or is disabled
            if not ai_sessions:
                generate_study_sessions(event)  # Existing function
                messages.info(request, 'Event created with automatic scheduling')
            else:
                messages.success(request, f'Event created with AI-powered learning plan ({len(ai_sessions)} tasks)')

            return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm()

    return render(request, 'events/event_form.html', {'form': form})
```

### Adding "Regenerate Plan" Button

In `event_detail` view, add option to regenerate with AI:

```python
@login_required
def event_regenerate_plan(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)

    # Delete existing pending sessions
    event.study_sessions.filter(status='pending').delete()

    # Generate new AI plan (force regenerate)
    ai_sessions = generate_ai_study_sessions(event, force_regenerate=True)

    if ai_sessions:
        messages.success(request, f'Learning plan regenerated with {len(ai_sessions)} new tasks')
    else:
        generate_study_sessions(event)  # Fallback
        messages.info(request, 'Plan regenerated with standard scheduling')

    return redirect('event_detail', pk=event.pk)
```

### Adding Re-Planning Alerts

In `event_detail` view, check for re-planning triggers:

```python
from ai.event_integration import check_for_replan_triggers, generate_replan_suggestions

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, user=request.user)

    # Check if re-planning is needed
    issue_type = check_for_replan_triggers(event)
    replan_suggestions = None

    if issue_type:
        replan_suggestions = generate_replan_suggestions(event, issue_type)

    context = {
        'event': event,
        'study_sessions': event.study_sessions.all().order_by('date', 'start_time'),
        'issue_type': issue_type,
        'replan_suggestions': replan_suggestions,
    }

    return render(request, 'events/event_detail.html', context)
```

## 🎨 UI Integration

### Displaying AI-Generated Tasks

Update `templates/events/event_detail.html`:

```html
<div class="card mb-4">
    <div class="card-header">
        <h5>Study Plan
            {% if ai_generated %}
            <span class="badge bg-success">AI-Generated</span>
            {% endif %}
        </h5>
    </div>
    <div class="card-body">
        {% for session in study_sessions %}
        <div class="session-card">
            <h6>{{ session.date|date:"M d, Y" }} - {{ session.start_time|time:"g:i A" }}</h6>
            <div class="suggested-content">
                {{ session.suggested_content|linebreaks }}
            </div>
            <small class="text-muted">
                Duration: {{ session.duration_minutes }} min
                | Status: {{ session.get_status_display }}
            </small>
        </div>
        {% endfor %}

        <button class="btn btn-outline-primary" onclick="regeneratePlan()">
            <i class="bi bi-arrow-clockwise"></i> Regenerate Plan with AI
        </button>
    </div>
</div>
```

### Displaying Re-Planning Suggestions

```html
{% if replan_suggestions %}
<div class="alert alert-warning">
    <h5><i class="bi bi-lightbulb"></i> AI Detected an Issue</h5>
    <p>Issue: {{ issue_type|title }}</p>

    <h6>Suggestions:</h6>
    <ul>
        {% for suggestion in replan_suggestions.suggestions %}
        <li>
            <strong>{{ suggestion.task_title }}</strong><br>
            {{ suggestion.reason }}<br>
            <small>Recommended duration: {{ suggestion.new_duration_minutes }} min</small>
        </li>
        {% endfor %}
    </ul>

    <button class="btn btn-primary" onclick="applyReplanSuggestions()">
        Apply Suggestions
    </button>
    <button class="btn btn-outline-secondary" onclick="dismissSuggestions()">
        Dismiss
    </button>
</div>
{% endif %}
```

## 📊 Metrics & Monitoring

### Track AI Effectiveness

The system should measure:

1. **Task completion rate**: AI-generated vs deterministic
2. **Average time overrun**: How accurate are AI duration estimates
3. **Event deadline success rate**: Do AI plans help students finish on time
4. **User acceptance**: How often do users regenerate or dismiss AI plans

### Logging

All AI interactions are logged:

```python
import logging
logger = logging.getLogger('ai')

# Logs include:
# - AI plan generation attempts
# - Success/failure status
# - Response parsing errors
# - Cache hits/misses
```

View logs:

```bash
# In settings.py, configure logging
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'ai_calls.log',
        },
    },
    'loggers': {
        'ai': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

## 🔒 Safety & Cost Control

### Rate Limiting

Implement caching and rate limits:

```python
from django.core.cache import cache
from django.utils import timezone

def rate_limit_ai_calls(user, max_calls_per_hour=10):
    """Limit AI calls per user"""
    cache_key = f'ai_calls_{user.id}_{timezone.now().hour}'
    calls = cache.get(cache_key, 0)

    if calls >= max_calls_per_hour:
        raise Exception("AI rate limit exceeded")

    cache.set(cache_key, calls + 1, timeout=3600)
```

### Cost Monitoring

Track API usage:

```python
# In services.py, log token usage
logger.info(f"AI call: {tokens_used} tokens, estimated cost: ${cost}")
```

### Fallback Strategy

System always has a deterministic fallback:

1. Try AI plan generation
2. If AI fails → Use `generate_study_sessions()` (existing function)
3. If AI is disabled → Always use deterministic
4. User can always manually edit or override

## 🧪 Testing

### Test with Mock Provider

```python
# In settings.py
AI_ENABLED = True
AI_PROVIDER = 'mock'
```

Mock provider returns valid sample data without API calls.

### Unit Tests

```python
from django.test import TestCase
from ai.services import AIService

class AIServiceTests(TestCase):
    def test_mock_provider(self):
        service = AIService()
        service.provider = 'mock'

        plan = service.generate_learning_plan(
            event_title="Math Exam",
            event_type="exam",
            event_date=datetime.now() + timedelta(days=7),
            prep_time_hours=6.0,
            subject="Algebra",
            description="Quadratic equations"
        )

        self.assertIsNotNone(plan)
        self.assertIn('tasks', plan)
        self.assertGreater(len(plan['tasks']), 0)
```

## 📚 Next Steps

### Phase 2 Enhancements

1. **User Feedback Loop**: Let users rate AI-generated plans
2. **Personalization**: Learn from user's completion patterns
3. **Multi-Language Support**: Translate AI prompts for Vietnamese users
4. **Advanced Re-Planning**: Automatically apply safe adjustments
5. **Analytics Dashboard**: Show AI effectiveness metrics

### Recommended Improvements

1. Add "AI Quality" rating to each generated plan
2. A/B test AI vs deterministic scheduling
3. Track which task types users complete most successfully
4. Adjust AI prompts based on user feedback
5. Implement progressive disclosure (show AI suggestions only when helpful)

## ❓ Troubleshooting

### AI Plan Not Generated

Check:
1. `AI_ENABLED = True` in settings
2. Valid API key configured
3. Check logs for error messages
4. Test with mock provider first

### JSON Parsing Errors

AI sometimes returns invalid JSON:
- Check prompt template formatting
- Add explicit "return only JSON" instruction
- Increase temperature for more deterministic responses
- Add retry logic with exponential backoff

### High API Costs

Solutions:
- Use caching (already implemented)
- Switch to cheaper models (gpt-3.5-turbo, claude-3-haiku)
- Implement stricter rate limiting
- Only regenerate on explicit user request

## 📖 References

- AI Requirements Document: `AI-req.txt`
- Django Caching: https://docs.djangoproject.com/en/4.2/topics/cache/
- OpenAI API: https://platform.openai.com/docs/api-reference
- Anthropic API: https://docs.anthropic.com/claude/reference/

---

**Implementation Date**: 2026-01-15
**Version**: 1.0
**Maintained By**: EduFlow AI Development Team
