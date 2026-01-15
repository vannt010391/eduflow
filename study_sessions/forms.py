from django import forms
from .models import StudySession

class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class StudySessionUpdateForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['suggested_content', 'status', 'notes']
        widgets = {
            'suggested_content': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
