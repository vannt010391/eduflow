from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    event_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    # Phase 3: Optional diagnostic test file upload
    diagnostic_file = forms.FileField(
        required=False,
        label='Diagnostic Test File (Optional)',
        help_text='Upload a diagnostic test (PDF, DOC, DOCX, or image: JPG, PNG) - Max 10MB',
        widget=forms.FileInput(attrs={
            'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png',
            'class': 'form-control'
        })
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

    def clean_diagnostic_file(self):
        """Validate diagnostic file upload."""
        file = self.cleaned_data.get('diagnostic_file')

        if file:
            # Check file size (10MB limit)
            if file.size > 10 * 1024 * 1024:  # 10MB in bytes
                raise forms.ValidationError('File size must be under 10MB.')

            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png']
            file_ext = file.name.lower()[file.name.rfind('.'):]

            if file_ext not in allowed_extensions:
                raise forms.ValidationError(
                    f'File type not allowed. Allowed types: PDF, DOC, DOCX, JPG, PNG'
                )

        return file
