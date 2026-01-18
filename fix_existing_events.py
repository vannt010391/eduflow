"""
Fix existing events that don't have study sessions
"""
import os
import sys

# Fix encoding for Vietnamese characters
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')

import django
django.setup()

from events.models import Event
from events.views import generate_study_sessions

print("="*60)
print("FIX EXISTING EVENTS - REGENERATE STUDY SESSIONS")
print("="*60)

events = Event.objects.all()
print(f"\nTotal events in database: {events.count()}")

for i, event in enumerate(events, 1):
    print(f"\n[Event {i}] {event.title}")
    print(f"  Event date: {event.event_date}")
    print(f"  Prep time: {event.estimated_prep_time} hours")

    # Check existing sessions
    existing_sessions = event.study_sessions.count()
    print(f"  Existing sessions: {existing_sessions}")

    if existing_sessions == 0:
        print(f"  [ACTION] Generating study sessions...")
        try:
            # Delete old sessions and regenerate
            event.study_sessions.all().delete()

            # Generate new sessions
            sessions = generate_study_sessions(event)

            print(f"  [OK] Generated {len(sessions)} study sessions!")

            # Show first 3 sessions
            if sessions:
                print(f"  First few sessions:")
                for session in sessions[:3]:
                    print(f"    - {session.date}: {session.duration_minutes} min")
                    if session.suggested_content:
                        title_line = session.suggested_content.split('\n')[0]
                        print(f"      {title_line[:50]}...")

        except Exception as e:
            print(f"  [ERROR] Failed to generate sessions: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"  [SKIP] Already has sessions")

print("\n" + "="*60)
print("FIX COMPLETE")
print("="*60)
print("\nRefresh your browser to see the updated events!")
print("The study sessions should now appear in the event detail page.")
