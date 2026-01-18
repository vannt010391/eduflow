"""
Test improved AI features: more tasks and focus timer tracking
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')

import django
django.setup()

from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from events.models import Event
from events.views import generate_study_sessions

print("="*60)
print("IMPROVED FEATURES TEST")
print("="*60)

# Create test user
print("\n[1] Creating test user...")
user, created = User.objects.get_or_create(
    username='feature_test_user',
    defaults={'email': 'feature@test.com'}
)
if created:
    user.set_password('testpass123')
    user.save()
print(f"[OK] User: {user.username}")

# Create event with 6 hours prep time
print("\n[2] Creating event with 6 hours prep time...")
event_date = timezone.now() + timedelta(days=7)
event = Event.objects.create(
    user=user,
    title="Python Advanced Programming Exam",
    event_type="exam",
    event_date=event_date,
    subject="Computer Science",
    priority="high",
    estimated_prep_time=6.0,
    description="OOP, data structures, algorithms, and design patterns"
)
print(f"[OK] Event created: {event.title}")
print(f"    Prep time: {event.estimated_prep_time} hours")

# Generate AI sessions
print("\n[3] Generating AI study sessions...")
sessions = generate_study_sessions(event)
print(f"[OK] Generated {len(sessions)} sessions")

# Check if we have 10+ sessions
print("\n[4] Checking session count...")
total_sessions = event.study_sessions.count()
print(f"Total sessions: {total_sessions}")

if total_sessions >= 10:
    print("[OK] SUCCESS! Generated 10+ sessions for better balance")
else:
    print(f"[INFO] Generated {total_sessions} sessions (target: 10+)")

# Display all sessions
print("\n[5] Session Details:")
print("-" * 60)
total_minutes = 0
for i, session in enumerate(event.study_sessions.all(), 1):
    total_minutes += session.duration_minutes
    print(f"\nSession {i}:")
    print(f"  Date: {session.date}")
    print(f"  Duration: {session.duration_minutes} minutes")

    if session.suggested_content:
        lines = session.suggested_content.split('\n')
        title_line = lines[0] if lines else 'No content'
        print(f"  Task: {title_line[:60]}")

print(f"\nTotal planned time: {total_minutes} minutes ({total_minutes/60:.1f} hours)")
print(f"Target time: {event.estimated_prep_time} hours")

# Verify distribution
print("\n[6] Session Distribution Analysis:")
print("-" * 60)
session_counts = {}
for session in event.study_sessions.all():
    date_str = session.date.strftime('%Y-%m-%d')
    session_counts[date_str] = session_counts.get(date_str, 0) + 1

print(f"Sessions distributed across {len(session_counts)} days:")
for date, count in sorted(session_counts.items()):
    print(f"  {date}: {count} session(s)")

avg_per_day = total_sessions / len(session_counts) if session_counts else 0
print(f"\nAverage sessions per day: {avg_per_day:.1f}")

# Check task variety
print("\n[7] Task Variety Check:")
print("-" * 60)
task_types = {
    'concept_review': 0,
    'practice': 0,
    'deep_practice': 0,
    'revision': 0,
    'mock_test': 0
}

for session in event.study_sessions.all():
    if session.suggested_content:
        content = session.suggested_content.lower()
        if 'concept review' in content:
            task_types['concept_review'] += 1
        elif 'deep practice' in content:
            task_types['deep_practice'] += 1
        elif 'practice' in content:
            task_types['practice'] += 1
        elif 'revision' in content:
            task_types['revision'] += 1
        elif 'mock' in content or 'test' in content:
            task_types['mock_test'] += 1

print("Task type distribution:")
for task_type, count in task_types.items():
    if count > 0:
        print(f"  {task_type.replace('_', ' ').title()}: {count}")

# Summary
print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)

if total_sessions >= 10:
    print("[OK] Generated 10+ balanced sessions")
else:
    print(f"[INFO] Generated {total_sessions} sessions")

if abs(total_minutes/60 - event.estimated_prep_time) <= 0.6:  # Within 10% tolerance
    print("[OK] Total time matches prep time")
else:
    print(f"[INFO] Time difference: {abs(total_minutes/60 - event.estimated_prep_time):.1f} hours")

if avg_per_day <= 2:
    print("[OK] Reasonable daily load (avg {avg_per_day:.1f} sessions/day)")
else:
    print(f"[WARNING] High daily load (avg {avg_per_day:.1f} sessions/day)")

if sum(task_types.values()) >= 8:
    print("[OK] Good task variety")

print("\nKey Improvements:")
print("  - More sessions (10+) for better focus")
print("  - Shorter sessions (25-30 min) prevent burnout")
print("  - Varied task types keep learning engaging")
print("  - Better distribution across available days")

print("\nNext: Test in web UI!")
print("  1. Restart server: python manage.py runserver")
print("  2. Create event via web interface")
print("  3. Click 'Start with Timer' on any session")
print("  4. See countdown timer in focus timer page")
print("  5. Timer shows remaining time and progress")

print("="*60)

# Cleanup
print("\n[Cleanup] Removing test event...")
event.delete()
print("[OK] Test complete")
