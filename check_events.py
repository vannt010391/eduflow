"""
Check events in database
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')

import django
django.setup()

from events.models import Event
from django.utils import timezone

print("="*60)
print("DATABASE EVENTS CHECK")
print("="*60)

events = Event.objects.all()
print(f"\nTotal events: {events.count()}")

for i, event in enumerate(events, 1):
    print(f"\n[Event {i}]")
    print(f"  Title: {event.title}")
    print(f"  Date: {event.event_date}")
    print(f"  Now: {timezone.now()}")
    print(f"  Days until: {event.days_until_event()}")
    print(f"  Prep time: {event.estimated_prep_time} hours")
    print(f"  Study sessions: {event.study_sessions.count()}")

    if event.study_sessions.count() > 0:
        print(f"  Session details:")
        for session in event.study_sessions.all()[:3]:
            print(f"    - {session.date}: {session.duration_minutes} min")

    # Check if event date is in the past
    if event.event_date < timezone.now():
        print(f"  [WARNING] Event date is in the PAST!")
        print(f"  This is why no sessions were generated.")

print("\n" + "="*60)
