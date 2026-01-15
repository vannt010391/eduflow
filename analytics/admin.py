from django.contrib import admin
from .models import DailyStudyLog, WeeklyStudyLog

@admin.register(DailyStudyLog)
class DailyStudyLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'total_focus_minutes', 'completed_sessions', 'total_sessions']
    list_filter = ['date']
    search_fields = ['user__username']
    date_hierarchy = 'date'

@admin.register(WeeklyStudyLog)
class WeeklyStudyLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'week_start', 'week_end', 'total_focus_minutes', 'events_completed', 'consistency_score']
    list_filter = ['week_start']
    search_fields = ['user__username']
    date_hierarchy = 'week_start'
