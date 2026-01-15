#!/usr/bin/env python
"""
Test script for EduFlow AI features

This script demonstrates the AI functionality with the mock provider.
Run this to validate the AI system works correctly before integrating
into the Django views.

Usage:
    python test_ai_features.py
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eduflow_ai.settings')
django.setup()

from ai.services import get_ai_service
from ai.schemas import validate_learning_plan


def test_plan_generation():
    """Test AI learning plan generation"""
    print("=" * 60)
    print("TEST 1: Learning Plan Generation")
    print("=" * 60)

    ai_service = get_ai_service()

    # Test data
    event_title = "Algebra Final Exam"
    event_type = "exam"
    event_date = datetime.now() + timedelta(days=7)
    prep_time_hours = 6.0
    subject = "Mathematics"
    description = "Quadratic equations, inequalities, and graphing parabolas"

    print(f"\nGenerating plan for: {event_title}")
    print(f"Event type: {event_type}")
    print(f"Days until event: 7")
    print(f"Preparation time: {prep_time_hours} hours")
    print(f"Subject: {subject}")
    print(f"Description: {description}")
    print("\nCalling AI service...")

    try:
        plan = ai_service.generate_learning_plan(
            event_title=event_title,
            event_type=event_type,
            event_date=event_date,
            prep_time_hours=prep_time_hours,
            subject=subject,
            description=description,
            daily_limit_minutes=480,
            focus_mode="Pomodoro"
        )

        if plan:
            print("\nSUCCESS! AI generated a learning plan:\n")
            print(f"Goal: {plan['goal_summary']}\n")
            print(f"Tasks ({len(plan['tasks'])}):")
            print("-" * 60)

            for i, task in enumerate(plan['tasks'], 1):
                print(f"\n{i}. {task['title']}")
                print(f"   Type: {task['task_type']}")
                print(f"   Duration: {task['suggested_duration_minutes']} minutes")
                print(f"   Difficulty: {task['difficulty']}")
                print(f"   Cognitive Load: {task['cognitive_load']}")
                if task.get('notes'):
                    print(f"   Notes: {task['notes']}")

            # Validate schema
            print("\n" + "=" * 60)
            print("Validating JSON schema...")
            validate_learning_plan(plan)
            print("[OK] Schema validation passed!")

            return True
        else:
            print("[FAIL] FAILED: AI service returned None")
            return False

    except Exception as e:
        print(f"[FAIL] ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_replan_suggestions():
    """Test AI re-planning suggestions"""
    print("\n\n" + "=" * 60)
    print("TEST 2: Adaptive Re-Planning Suggestions")
    print("=" * 60)

    ai_service = get_ai_service()

    # Test data
    event_title = "Physics Quiz"
    tasks_data = [
        {
            'title': 'Practice problems and exercises',
            'planned_duration': 45,
            'actual_duration': 65,
            'status': 'completed'
        },
        {
            'title': 'Deep practice: Complex scenarios',
            'planned_duration': 45,
            'actual_duration': 70,
            'status': 'completed'
        },
        {
            'title': 'Mock test preparation',
            'planned_duration': 60,
            'actual_duration': None,
            'status': 'skipped'
        }
    ]
    issue_type = 'tasks_overrunning'
    performance_data = {
        'avg_overrun_percent': 48,
        'skipped_count': 1,
        'completion_percent': 45,
        'days_remaining': 3
    }

    print(f"\nAnalyzing event: {event_title}")
    print(f"Issue detected: {issue_type}")
    print(f"Performance data: {performance_data}")
    print("\nCalling AI service...")

    try:
        suggestions = ai_service.suggest_replan(
            event_title=event_title,
            tasks_data=tasks_data,
            issue_type=issue_type,
            performance_data=performance_data
        )

        if suggestions:
            print("\n[OK] SUCCESS! AI generated re-planning suggestions:\n")
            print(f"Issue: {suggestions['issue_detected']}\n")
            print(f"Suggestions ({len(suggestions['suggestions'])}):")
            print("-" * 60)

            for i, sugg in enumerate(suggestions['suggestions'], 1):
                print(f"\n{i}. Task: {sugg['task_title']}")
                print(f"   Action: {sugg['action']}")
                print(f"   New Duration: {sugg['new_duration_minutes']} minutes")
                if sugg.get('reason'):
                    print(f"   Reason: {sugg['reason']}")

            return True
        else:
            print("[FAIL] FAILED: AI service returned None")
            return False

    except Exception as e:
        print(f"[FAIL] ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_ai_configuration():
    """Test AI service configuration"""
    print("\n\n" + "=" * 60)
    print("TEST 3: AI Service Configuration")
    print("=" * 60)

    from django.conf import settings

    print("\nChecking Django settings...")
    print(f"AI_ENABLED: {getattr(settings, 'AI_ENABLED', 'Not set')}")
    print(f"AI_PROVIDER: {getattr(settings, 'AI_PROVIDER', 'Not set')}")
    print(f"AI_MODEL: {getattr(settings, 'AI_MODEL', 'Not set')}")

    ai_service = get_ai_service()
    print(f"\nAI Service instance:")
    print(f"Provider: {ai_service.provider}")
    print(f"Model: {ai_service.model}")
    print(f"Enabled: {ai_service.enabled}")

    if ai_service.provider == 'mock':
        print("\n[OK] Using mock provider (good for testing)")
    elif ai_service.provider in ['openai', 'anthropic']:
        if ai_service.api_key:
            print(f"\n[OK] API key configured for {ai_service.provider}")
        else:
            print(f"\n[WARN]  WARNING: {ai_service.provider} selected but no API key")

    return True


def main():
    """Run all tests"""
    print("\nEduFlow AI - AI Features Test Suite\n")

    results = {
        'Configuration Check': test_ai_configuration(),
        'Learning Plan Generation': test_plan_generation(),
        'Re-Planning Suggestions': test_replan_suggestions(),
    }

    print("\n\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)

    for test_name, passed in results.items():
        status = "[OK] PASSED" if passed else "[FAIL] FAILED"
        print(f"{test_name}: {status}")

    all_passed = all(results.values())

    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED!")
        print("\nNext steps:")
        print("1. Review the generated plans above")
        print("2. Integrate into events/views.py")
        print("3. Test in the Django web interface")
        print("4. Configure a real AI provider (OpenAI/Anthropic)")
    else:
        print("WARNING: SOME TESTS FAILED")
        print("\nPlease review errors above and fix before proceeding.")

    print("=" * 60 + "\n")

    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())
