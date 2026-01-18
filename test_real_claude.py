"""
Test Real Claude API - Generate Study Sessions
"""
import os
import sys
import codecs
from datetime import timedelta

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')

import django
django.setup()

from django.utils import timezone
from django.contrib.auth import get_user_model
from events.models import Event
from ai.event_integration import generate_ai_study_sessions

User = get_user_model()

print("=" * 80)
print("REAL CLAUDE API TEST - Study Session Generation")
print("=" * 80)

# Get or create test user
print("\n[1] Setting up test user...")
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
    print(f"✅ Created test user: {user.username}")
else:
    print(f"✅ Using existing user: {user.username}")

# Create test event
print("\n[2] Creating test event...")
event_date = timezone.now() + timedelta(days=14)
event = Event.objects.create(
    user=user,
    title="Test Claude API - Thi Toán",
    event_type='exam',
    event_date=event_date,
    estimated_prep_time=8.0,
    subject="Toán học",
    priority='high',
    description="Kiểm tra Claude API có thể tạo study plan thông minh cho kỳ thi Toán"
)

print(f"✅ Event created:")
print(f"   - Title: {event.title}")
print(f"   - Date: {event.event_date.strftime('%Y-%m-%d')}")
print(f"   - Prep time: {event.estimated_prep_time} hours")
print(f"   - Subject: {event.subject}")

# Generate study sessions with Claude
print("\n[3] Calling Claude API to generate study sessions...")
print("⚠️  This will make a REAL API call and use credits (~$0.009)")
print("⏳ Generating...")

try:
    sessions = generate_ai_study_sessions(event, force_regenerate=True)

    print(f"\n✅ SUCCESS! Claude generated {len(sessions)} study sessions!")
    print("\n" + "=" * 80)
    print("GENERATED STUDY SESSIONS")
    print("=" * 80)

    for i, session in enumerate(sessions, 1):
        print(f"\n📝 Session {i}:")
        print(f"   Date: {session.date.strftime('%Y-%m-%d')}")
        print(f"   Time: {session.start_time.strftime('%H:%M')}")
        print(f"   Duration: {session.duration_minutes} min")
        print(f"   Status: {session.status}")
        if session.suggested_content:
            content_preview = session.suggested_content[:150] + "..." if len(session.suggested_content) > 150 else session.suggested_content
            print(f"   Content: {content_preview}")

    print("\n" + "=" * 80)
    print("📊 SUMMARY")
    print("=" * 80)
    print(f"✅ Total sessions: {len(sessions)}")
    print(f"✅ Event ID: {event.id}")
    print(f"✅ User: {user.username}")

    # Calculate total time
    total_minutes = sum(s.duration_minutes for s in sessions)
    total_hours = total_minutes / 60
    print(f"✅ Total study time: {total_minutes} min ({total_hours:.1f} hours)")

    # Calculate date range
    if sessions:
        first_date = min(s.date for s in sessions)
        last_date = max(s.date for s in sessions)
        print(f"✅ Date range: {first_date.strftime('%Y-%m-%d')} to {last_date.strftime('%Y-%m-%d')}")
        print(f"✅ Days spanned: {(last_date - first_date).days + 1} days")

    print("\n" + "=" * 80)
    print("🎉 CLAUDE API TEST SUCCESSFUL!")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Check web UI: http://127.0.0.1:8000/events/")
    print("  2. Verify session quality")
    print("  3. Check Anthropic dashboard for usage")
    print("  4. Monitor costs")

    print(f"\n🔗 View event: http://127.0.0.1:8000/events/{event.id}/")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

    print("\n" + "=" * 80)
    print("🔧 TROUBLESHOOTING")
    print("=" * 80)
    print("\nPossible issues:")
    print("  1. Invalid API key")
    print("  2. Insufficient credits")
    print("  3. Network connection")
    print("  4. Rate limit exceeded")
    print("\nCheck:")
    print("  - API key in .env file")
    print("  - Anthropic console: https://console.anthropic.com/")
    print("  - Payment method added")
    print("  - Internet connection")

print("\n" + "=" * 80)
