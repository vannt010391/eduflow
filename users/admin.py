from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'student_id', 'grade_level']
    search_fields = ['user__username', 'student_id']
    readonly_fields = ['created_at', 'updated_at']
