from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'event_date', 'priority', 'user', 'completion_percentage']
    list_filter = ['event_type', 'priority', 'event_date']
    search_fields = ['title', 'subject', 'user__username']
    date_hierarchy = 'event_date'
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'title', 'event_type', 'subject')
        }),
        ('Schedule', {
            'fields': ('event_date', 'priority', 'estimated_prep_time')
        }),
        ('Details', {
            'fields': ('description',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
