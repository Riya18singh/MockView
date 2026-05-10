from django.contrib import admin
from .models import EvaluationReport, UserProgress


@admin.register(EvaluationReport)
class EvaluationReportAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'overall_score', 'technical_score',
        'communication_score', 'generated_at'
    ]
    list_filter = ['user']


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'total_interviews',
        'average_score', 'best_score'
    ]