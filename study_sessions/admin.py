from django.contrib import admin
from .models import StudySession

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['event', 'date', 'start_time', 'duration_minutes', 'status']
    list_filter = ['status', 'date']
    search_fields = ['event__title', 'suggested_content']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at']
