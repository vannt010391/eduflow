from django.contrib import admin
from .models import FocusModel, FocusSession, BreakSession, UserPreference

@admin.register(FocusModel)
class FocusModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_type', 'focus_duration', 'break_duration']
    list_filter = ['model_type']

@admin.register(FocusSession)
class FocusSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_time', 'duration_minutes', 'completed']
    list_filter = ['completed', 'start_time']
    search_fields = ['user__username']
    date_hierarchy = 'start_time'

@admin.register(BreakSession)
class BreakSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'start_time', 'recommended_duration', 'actual_duration', 'completed']
    list_filter = ['completed', 'start_time']
    search_fields = ['user__username']
    date_hierarchy = 'start_time'

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'default_focus_model', 'daily_study_limit', 'enable_overload_alerts']
    search_fields = ['user__username']
