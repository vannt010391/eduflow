"""
Cleanup test data and verify AI is working
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')

import django
django.setup()

from events.models import Event
from django.contrib.auth.models import User

print("="*60)
print("CLEANUP TEST DATA")
print("="*60)

# Show current state
print("\n[1] Current database state:")
all_events = Event.objects.all()
print(f"Total events: {all_events.count()}")

# List all events
for event in all_events:
    print(f"  - ID {event.id}: {event.title} ({event.user.username}) - {event.study_sessions.count()} sessions")

# Ask for confirmation
print("\n[2] Cleanup options:")
print("This will delete test events created during testing.")
print("Events with these markers will be deleted:")
print("  - '[DIAGNOSTIC TEST]' in title")
print("  - 'AI Test' in title")
print("  - 'Python Programming Exam' (test events)")
print("  - User 'event_test_user' or 'ai_test_user'")

# Delete test events
test_markers = ['[DIAGNOSTIC TEST]', 'AI Test', 'Python Programming']
test_users = ['event_test_user', 'ai_test_user', 'test_ai_user']

deleted_count = 0

for event in all_events:
    should_delete = False

    # Check if event has test markers
    for marker in test_markers:
        if marker in event.title:
            should_delete = True
            break

    # Check if user is a test user
    if event.user.username in test_users:
        should_delete = True

    if should_delete:
        print(f"\nDeleting: {event.title}")
        event.delete()
        deleted_count += 1

print(f"\n[OK] Deleted {deleted_count} test events")

# Show final state
remaining = Event.objects.all()
print(f"\n[3] Remaining events: {remaining.count()}")
for event in remaining:
    print(f"  - {event.title} ({event.user.username})")

# Clean up test users
print("\n[4] Cleanup test users...")
test_user_count = User.objects.filter(username__in=test_users).count()
if test_user_count > 0:
    User.objects.filter(username__in=test_users).delete()
    print(f"[OK] Deleted {test_user_count} test users")
else:
    print("[INFO] No test users to delete")

print("\n" + "="*60)
print("CLEANUP COMPLETE")
print("="*60)
print("\nDatabase is now clean!")
print("Next steps:")
print("1. Make sure Django server is running")
print("2. Create a NEW event via the web interface")
print("3. Check that AI-generated tasks appear")
print("="*60)
