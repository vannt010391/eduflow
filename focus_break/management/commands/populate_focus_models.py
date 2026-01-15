from django.core.management.base import BaseCommand
from focus_break.models import FocusModel

class Command(BaseCommand):
    help = 'Populate initial focus models'

    def handle(self, *args, **kwargs):
        focus_models = [
            {
                'name': 'Pomodoro',
                'model_type': 'pomodoro',
                'focus_duration': 25,
                'break_duration': 5,
                'description': 'The classic Pomodoro technique: 25 minutes of focused work followed by a 5-minute break.'
            },
            {
                'name': 'Extended Focus',
                'model_type': 'extended',
                'focus_duration': 45,
                'break_duration': 10,
                'description': 'Extended focus sessions for deeper concentration: 45 minutes of work followed by a 10-minute break.'
            },
            {
                'name': 'Deep Work',
                'model_type': 'deep_work',
                'focus_duration': 60,
                'break_duration': 15,
                'description': 'Deep work sessions for maximum productivity: 60 minutes of intense focus followed by a 15-minute break.'
            }
        ]

        for model_data in focus_models:
            FocusModel.objects.get_or_create(
                model_type=model_data['model_type'],
                defaults=model_data
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated focus models'))
