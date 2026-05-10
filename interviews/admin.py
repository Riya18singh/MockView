from django.contrib import admin
from .models import InterviewSession, Message


@admin.register(InterviewSession)
class InterviewSessionAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'interview_type', 'difficulty',
        'target_company', 'status', 'started_at'
    ]
    list_filter = [
        'status', 'interview_type',
        'difficulty', 'target_company'
    ]
    search_fields = ['user__username']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'role', 'score', 'timestamp']
    list_filter = ['role']