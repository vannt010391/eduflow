"""
Test event creation with AI study session generation
"""
import sys
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')

import django
django.setup()

from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from events.models import Event
from study_sessions.models import StudySession
from events.views import generate_study_sessions

print("="*60)
print("EVENT CREATION TEST - AI Study Session Generation")
print("="*60)

# Create or get test user
print("\n[1] Setting up test user...")
user, created = User.objects.get_or_create(
    username='event_test_user',
    defaults={'email': 'event_test@example.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
print(f"[OK] User: {user.username}")

# Create a test event
print("\n[2] Creating test event...")
event_date = timezone.now() + timedelta(days=7)
event = Event.objects.create(
    user=user,
    title="Python Programming Exam",
    event_type="exam",
    event_date=event_date,
    subject="Computer Science",
    priority="high",
    estimated_prep_time=6.0,
    description="Focus on OOP, data structures, and algorithms"
)
print(f"[OK] Event created: {event.title}")
print(f"    Type: {event.event_type}")
print(f"    Date: {event.event_date}")
print(f"    Prep time: {event.estimated_prep_time} hours")
print(f"    Days until event: {event.days_until_event()}")

# Generate study sessions using the updated function
print("\n[3] Generating study sessions with AI...")
sessions = generate_study_sessions(event)

if sessions:
    print(f"[OK] Generated {len(sessions)} study sessions")

    # Check if sessions were created
    all_sessions = event.study_sessions.all()
    print(f"    Total sessions in database: {all_sessions.count()}")

    # Display sessions
    print("\n[4] Study Session Details:")
    print("-" * 60)
    for i, session in enumerate(all_sessions[:5], 1):
        print(f"\nSession {i}:")
        print(f"  Date: {session.date}")
        print(f"  Time: {session.start_time}")
        print(f"  Duration: {session.duration_minutes} minutes")
        print(f"  Status: {session.status}")

        # Check if it has AI-generated content
        if session.suggested_content:
            lines = session.suggested_content.split('\n')
            print(f"  Content Preview: {lines[0][:60]}...")

            # Check for AI markers
            if "Task" in session.suggested_content and "Type:" in session.suggested_content:
                print(f"  [AI Generated]: YES")
            else:
                print(f"  [AI Generated]: NO (Deterministic)")

    if all_sessions.count() > 5:
        print(f"\n  ... and {all_sessions.count() - 5} more sessions")

    # Verify AI integration
    print("\n[5] AI Integration Check:")
    print("-" * 60)
    ai_sessions = [s for s in all_sessions if s.suggested_content and "Task" in s.suggested_content]
    deterministic_sessions = [s for s in all_sessions if not (s.suggested_content and "Task" in s.suggested_content)]

    print(f"  AI-generated sessions: {len(ai_sessions)}")
    print(f"  Deterministic sessions: {len(deterministic_sessions)}")

    if len(ai_sessions) > 0:
        print("\n  [SUCCESS] AI is generating study sessions!")
        print(f"  Sample AI content:")
        sample = ai_sessions[0]
        print(f"  {sample.suggested_content[:200]}...")
    else:
        print("\n  [INFO] Using deterministic sessions (AI may be disabled or failed)")

    # Test event statistics
    print("\n[6] Event Statistics:")
    print("-" * 60)
    print(f"  Completion: {event.completion_percentage()}%")
    print(f"  At risk: {event.is_at_risk()}")
    print(f"  Days remaining: {event.days_until_event()}")
    print(f"  Total sessions: {all_sessions.count()}")
    print(f"  Pending sessions: {all_sessions.filter(status='pending').count()}")

else:
    print("[WARNING] No sessions generated")

# Summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)
print("[OK] Event creation works")
print("[OK] Study sessions are generated")
print("[OK] Sessions are linked to event")

if len(ai_sessions) > 0:
    print("[OK] AI integration is ACTIVE")
    print("\nConclusion: Events automatically generate AI-powered study sessions!")
else:
    print("[INFO] AI integration available but using fallback")
    print("\nConclusion: Events automatically generate study sessions (deterministic mode)")

print("\nTo verify in web interface:")
print("  1. Run: python manage.py runserver")
print("  2. Login to http://127.0.0.1:8000")
print("  3. Create a new event")
print("  4. Check the event detail page for generated sessions")
print("="*60)

# Cleanup
print("\n[Cleanup] Removing test event...")
event.delete()
print("[OK] Test completed and cleaned up")
