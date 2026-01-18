"""
Diagnose why UI is not showing AI-generated tasks
"""
import sys
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')

import django
django.setup()

from django.contrib.auth.models import User
from events.models import Event
from study_sessions.models import StudySession
from django.utils import timezone
from datetime import timedelta

print("="*60)
print("UI ISSUE DIAGNOSTIC")
print("="*60)

# Check if there are any existing events
print("\n[1] Checking existing events...")
all_events = Event.objects.all()
print(f"Total events in database: {all_events.count()}")

if all_events.count() > 0:
    print("\nRecent events:")
    for event in all_events.order_by('-created_at')[:3]:
        print(f"  - {event.title} (User: {event.user.username})")
        print(f"    Created: {event.created_at}")
        print(f"    Sessions: {event.study_sessions.count()}")

        if event.study_sessions.count() > 0:
            # Check first session content
            first_session = event.study_sessions.first()
            print(f"    First session content preview:")
            if first_session.suggested_content:
                content_preview = first_session.suggested_content[:100]
                print(f"    '{content_preview}...'")

                # Check if AI-generated
                if "Task" in first_session.suggested_content and "Type:" in first_session.suggested_content:
                    print(f"    [AI GENERATED] YES")
                else:
                    print(f"    [AI GENERATED] NO (deterministic)")
        print()

# Check AI configuration
print("\n[2] Checking AI configuration...")
from django.conf import settings
print(f"AI_ENABLED: {settings.AI_ENABLED}")
print(f"AI_PROVIDER: {settings.AI_PROVIDER}")

# Test AI service
print("\n[3] Testing AI service...")
try:
    from ai.services import get_ai_service
    ai_service = get_ai_service()
    print(f"[OK] AI Service initialized")
    print(f"    Provider: {ai_service.provider}")
    print(f"    Enabled: {ai_service.enabled}")
except Exception as e:
    print(f"[ERROR] AI Service failed: {e}")

# Test event creation programmatically
print("\n[4] Testing programmatic event creation...")
user = User.objects.first()
if user:
    print(f"Using user: {user.username}")

    # Create test event
    test_event = Event.objects.create(
        user=user,
        title="[DIAGNOSTIC TEST] Sample Event",
        event_type="exam",
        event_date=timezone.now() + timedelta(days=5),
        subject="Test Subject",
        priority="medium",
        estimated_prep_time=4.0,
        description="Testing AI generation"
    )
    print(f"[OK] Created test event: {test_event.title}")

    # Generate sessions
    from events.views import generate_study_sessions
    sessions = generate_study_sessions(test_event)

    print(f"[OK] Generated {len(sessions)} sessions")

    # Check sessions
    all_sessions = test_event.study_sessions.all()
    print(f"    Sessions in database: {all_sessions.count()}")

    if all_sessions.count() > 0:
        sample = all_sessions.first()
        print(f"\n    Sample session content:")
        print(f"    '{sample.suggested_content[:200]}...'")

        if "Task" in sample.suggested_content:
            print(f"\n    [SUCCESS] AI is generating content!")
        else:
            print(f"\n    [INFO] Using deterministic fallback")

    # Clean up
    test_event.delete()
    print(f"\n[Cleanup] Test event deleted")
else:
    print("[ERROR] No users found in database")

# Check view imports
print("\n[5] Checking view imports...")
try:
    from events.views import generate_ai_study_sessions
    print("[OK] generate_ai_study_sessions imported successfully")
except ImportError as e:
    print(f"[ERROR] Cannot import: {e}")

# Summary
print("\n" + "="*60)
print("DIAGNOSTIC SUMMARY")
print("="*60)

print("\nPossible issues:")
print("1. Server not restarted after code changes")
print("2. Template cache needs clearing")
print("3. Browser cache needs refresh")
print("4. Session data cached")

print("\nSolutions to try:")
print("1. Restart Django server:")
print("   - Stop: Ctrl+C")
print("   - Start: python manage.py runserver")
print("\n2. Hard refresh browser:")
print("   - Windows/Linux: Ctrl+Shift+R")
print("   - Mac: Cmd+Shift+R")
print("\n3. Clear browser cache and cookies")
print("\n4. Try incognito/private window")
print("\n5. Check browser console for errors (F12)")

print("="*60)
