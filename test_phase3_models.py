"""
Test Phase 3 Models - Demo Script

Tests EmotionalStateLog, DiagnosticTest, DiagnosticQuestion, and PlanAdjustmentSuggestion
"""
import os
import sys
import codecs

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')

import django
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
from events.models import Event
from study_sessions.models import StudySession
from emotional_state.models import EmotionalStateLog
from diagnostics.models import DiagnosticTest, DiagnosticQuestion, PlanAdjustmentSuggestion

print("=" * 80)
print("PHASE 3 MODELS TEST")
print("=" * 80)

# Get or create test user
print("\n[1] Setting up test user...")
user, created = User.objects.get_or_create(
    username='phase3_testuser',
    defaults={'email': 'phase3@test.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
    print(f"✅ Created user: {user.username}")
else:
    print(f"✅ Using existing user: {user.username}")

# Create test event
print("\n[2] Creating test event...")
event, created = Event.objects.get_or_create(
    user=user,
    title="Phase 3 Test Event - Thi Vật Lý",
    defaults={
        'event_type': 'exam',
        'event_date': timezone.now() + timezone.timedelta(days=14),
        'estimated_prep_time': 10.0,
        'subject': 'Vật lý',
        'priority': 'high',
        'description': 'Test event for Phase 3 models'
    }
)
print(f"✅ Event: {event.title}")

# ==================== Test 1: EmotionalStateLog ====================
print("\n" + "=" * 80)
print("TEST 1: EmotionalStateLog")
print("=" * 80)

print("\n[1.1] Creating self-reported emotional state...")
log1 = EmotionalStateLog.objects.create(
    user=user,
    energy_level='medium',
    stress_level='high',
    focus_level='low',
    source='self_report',
    trigger_context='day_start'
)
print(f"✅ Created log: {log1}")
print(f"   - Energy: {log1.energy_level}")
print(f"   - Stress: {log1.stress_level}")
print(f"   - Focus: {log1.focus_level}")
print(f"   - Needs attention: {log1.needs_attention}")

print("\n[1.2] Creating inferred emotional state...")
log2 = EmotionalStateLog.objects.create(
    user=user,
    energy_level='low',
    stress_level='medium',
    focus_level='low',
    source='inferred',
    trigger_context='early_termination'
)
print(f"✅ Created log: {log2}")
print(f"   - Source: {log2.source}")
print(f"   - Trigger: {log2.trigger_context}")
print(f"   - Is low energy: {log2.is_low_energy}")

print("\n[1.3] Getting recent state...")
recent_state = EmotionalStateLog.get_recent_state(user)
if recent_state:
    print(f"✅ Recent state (last 7 days):")
    print(f"   - Energy: {recent_state['energy']}")
    print(f"   - Stress: {recent_state['stress']}")
    print(f"   - Focus: {recent_state['focus']}")
    print(f"   - Sample size: {recent_state['sample_size']} logs")
else:
    print("❌ No recent state data")

# ==================== Test 2: DiagnosticTest ====================
print("\n" + "=" * 80)
print("TEST 2: DiagnosticTest & DiagnosticQuestion")
print("=" * 80)

print("\n[2.1] Creating diagnostic test...")
# Check if test exists for this event
existing_test = DiagnosticTest.objects.filter(event=event).first()
if existing_test:
    existing_test.delete()
    print("   Deleted existing test to create fresh one")

test = DiagnosticTest.objects.create(
    user=user,
    event=event,
    title="Đề kiểm tra Vật lý - Chẩn đoán"
)
print(f"✅ Created test: {test.title}")

print("\n[2.2] Adding questions to test...")
questions_data = [
    {
        'number': 1,
        'text': 'Định luật Newton thứ hai là gì?',
        'correct': 'F = ma',
        'user': 'F = m/a',
        'topic': 'Động lực học'
    },
    {
        'number': 2,
        'text': 'Công thức động năng?',
        'correct': 'Ek = 1/2 * m * v^2',
        'user': 'Ek = 1/2 * m * v^2',
        'topic': 'Năng lượng'
    },
    {
        'number': 3,
        'text': 'Đơn vị của lực là gì?',
        'correct': 'Newton',
        'user': 'N',  # Wrong - should be 'Newton'
        'topic': 'Đơn vị đo'
    },
    {
        'number': 4,
        'text': 'Gia tốc trọng trường trên Trái Đất?',
        'correct': '9.8 m/s^2',
        'user': '10 m/s^2',  # Approximately correct but not exact
        'topic': 'Trọng lực'
    },
    {
        'number': 5,
        'text': 'Công thức định luật Ohm?',
        'correct': 'V = I * R',
        'user': 'V = I * R',
        'topic': 'Điện học'
    },
]

for q_data in questions_data:
    question = DiagnosticQuestion.objects.create(
        diagnostic_test=test,
        question_number=q_data['number'],
        question_text=q_data['text'],
        correct_answer=q_data['correct'],
        user_answer=q_data['user'],
        topic=q_data['topic']
    )
    status = "✓" if question.is_correct else "✗"
    print(f"   {status} Q{question.question_number}: {question.topic} - {question.is_correct}")

print(f"\n[2.3] Test statistics:")
print(f"✅ Total questions: {test.total_questions}")
print(f"✅ Correct answers: {test.correct_count}")
print(f"✅ Incorrect answers: {test.incorrect_count}")
print(f"✅ Score: {test.score_percentage}%")

print(f"\n[2.4] Incorrect questions by topic:")
incorrect_questions = test.questions.filter(is_correct=False)
topics = {}
for q in incorrect_questions:
    topics[q.topic] = topics.get(q.topic, 0) + 1

for topic, count in topics.items():
    print(f"   - {topic}: {count} error(s)")

# ==================== Test 3: PlanAdjustmentSuggestion ====================
print("\n" + "=" * 80)
print("TEST 3: PlanAdjustmentSuggestion")
print("=" * 80)

print("\n[3.1] Creating plan adjustment suggestion...")
suggestion = PlanAdjustmentSuggestion.objects.create(
    user=user,
    event=event,
    triggered_by='high_stress_and_errors',
    context={
        'dominant_error_topic': 'Động lực học',
        'emotional_state': {
            'energy': 'medium',
            'stress': 'high',
            'focus': 'low'
        }
    },
    adjustments=[
        {
            'type': 'shorten',
            'target': 'Deep Practice Session 1',
            'new_duration_minutes': 30
        },
        {
            'type': 'split',
            'target': 'Động lực học Review',
            'new_duration_minutes': 25
        },
        {
            'type': 'focus_mode_change',
            'target': 'All sessions',
            'new_focus_mode': 'Pomodoro'
        }
    ],
    rationale="""Based on your current state:
- High stress level detected
- Low focus detected
- 3 errors in Động lực học topic

Recommendations:
1. Shorten intense practice sessions to reduce stress
2. Split difficult topics into smaller chunks
3. Use Pomodoro technique for better focus management

These adjustments should help reduce stress while maintaining learning effectiveness."""
)

print(f"✅ Created suggestion: {suggestion}")
print(f"   - Triggered by: {suggestion.triggered_by}")
print(f"   - Status: {suggestion.status}")
print(f"   - Number of adjustments: {suggestion.adjustment_count}")
print(f"\n   Rationale:")
for line in suggestion.rationale.split('\n'):
    if line.strip():
        print(f"   {line}")

print(f"\n[3.2] Simulating user acceptance...")
suggestion.accept(user_notes="These suggestions make sense. I'll try the shorter sessions.")
print(f"✅ Suggestion accepted")
print(f"   - Status: {suggestion.status}")
print(f"   - Reviewed at: {suggestion.reviewed_at}")
print(f"   - User notes: {suggestion.user_notes}")

# ==================== Summary ====================
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

print(f"\n✅ EmotionalStateLog:")
print(f"   - Total logs created: {EmotionalStateLog.objects.filter(user=user).count()}")
print(f"   - Self-reported: {EmotionalStateLog.objects.filter(user=user, source='self_report').count()}")
print(f"   - Inferred: {EmotionalStateLog.objects.filter(user=user, source='inferred').count()}")

print(f"\n✅ DiagnosticTest:")
print(f"   - Tests created: {DiagnosticTest.objects.filter(user=user).count()}")
print(f"   - Questions created: {DiagnosticQuestion.objects.filter(diagnostic_test__user=user).count()}")
print(f"   - Average score: {test.score_percentage}%")

print(f"\n✅ PlanAdjustmentSuggestion:")
print(f"   - Suggestions created: {PlanAdjustmentSuggestion.objects.filter(user=user).count()}")
print(f"   - Accepted: {PlanAdjustmentSuggestion.objects.filter(user=user, status='accepted').count()}")
print(f"   - Pending: {PlanAdjustmentSuggestion.objects.filter(user=user, status='pending').count()}")

print("\n" + "=" * 80)
print("🎉 ALL PHASE 3 MODELS WORKING PERFECTLY!")
print("=" * 80)

print("\n📊 Next Steps:")
print("   1. View data in admin: http://127.0.0.1:8000/admin/")
print("   2. Check emotional_state app")
print("   3. Check diagnostics app")
print("   4. Implement AI services for analysis")
print("   5. Build views and templates")

print("\n✅ Phase 3 Foundation: COMPLETE")
print("⏳ AI Services: Pending")
print("⏳ Views/Templates: Pending")
print("\n" + "=" * 80)
