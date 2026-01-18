from django.contrib import admin
from .models import DiagnosticTest, DiagnosticQuestion, PlanAdjustmentSuggestion


class DiagnosticQuestionInline(admin.TabularInline):
    model = DiagnosticQuestion
    extra = 1
    fields = ['question_number', 'question_text', 'correct_answer', 'user_answer', 'topic', 'is_correct', 'error_type']
    readonly_fields = ['is_correct']


@admin.register(DiagnosticTest)
class DiagnosticTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'event', 'total_questions', 'score_percentage', 'is_analyzed', 'created_at']
    list_filter = ['analyzed_at', 'created_at']
    search_fields = ['title', 'user__username', 'event__title']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at', 'analyzed_at']
    inlines = [DiagnosticQuestionInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'event', 'title', 'uploaded_file')
        }),
        ('Analysis', {
            'fields': ('analysis_result', 'analyzed_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def score_percentage(self, obj):
        return f"{obj.score_percentage}%"
    score_percentage.short_description = 'Score'


@admin.register(DiagnosticQuestion)
class DiagnosticQuestionAdmin(admin.ModelAdmin):
    list_display = ['diagnostic_test', 'question_number', 'topic', 'is_correct', 'error_type']
    list_filter = ['is_correct', 'error_type', 'topic']
    search_fields = ['question_text', 'topic']
    readonly_fields = ['is_correct']


@admin.register(PlanAdjustmentSuggestion)
class PlanAdjustmentSuggestionAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'triggered_by', 'status', 'adjustment_count', 'triggered_at']
    list_filter = ['status', 'triggered_by', 'triggered_at']
    search_fields = ['user__username', 'event__title', 'rationale']
    date_hierarchy = 'triggered_at'
    readonly_fields = ['triggered_at', 'reviewed_at']

    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'event', 'triggered_by', 'triggered_at')
        }),
        ('AI Suggestion', {
            'fields': ('context', 'adjustments', 'rationale')
        }),
        ('User Decision', {
            'fields': ('status', 'reviewed_at', 'user_notes')
        }),
    )

    def adjustment_count(self, obj):
        return obj.adjustment_count
    adjustment_count.short_description = '# Adjustments'
