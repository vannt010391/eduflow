from django.contrib import admin
from .models import EmotionalStateLog


@admin.register(EmotionalStateLog)
class EmotionalStateLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'timestamp', 'energy_level', 'stress_level', 'focus_level', 'source', 'needs_attention']
    list_filter = ['source', 'energy_level', 'stress_level', 'focus_level', 'timestamp']
    search_fields = ['user__username', 'trigger_context']
    date_hierarchy = 'timestamp'
    readonly_fields = ['timestamp']

    fieldsets = (
        ('User Info', {
            'fields': ('user', 'timestamp', 'source', 'trigger_context')
        }),
        ('Emotional State', {
            'fields': ('energy_level', 'stress_level', 'focus_level')
        }),
        ('Context', {
            'fields': ('study_session',),
            'classes': ('collapse',)
        }),
    )

    def needs_attention(self, obj):
        return obj.needs_attention
    needs_attention.boolean = True
    needs_attention.short_description = 'Needs Attention'
