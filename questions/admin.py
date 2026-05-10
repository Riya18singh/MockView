from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'question_text', 'category',
        'difficulty', 'company', 'times_asked'
    ]
    list_filter = ['category', 'difficulty', 'company']
    search_fields = ['question_text', 'tags']