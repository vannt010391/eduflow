from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    event_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Event
        fields = ['title', 'event_type', 'event_date', 'subject', 'priority', 'estimated_prep_time', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'estimated_prep_time': 'Enter total preparation time needed in hours (e.g., 10 for 10 hours)',
        }
