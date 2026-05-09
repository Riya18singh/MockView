from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'username', 'email', 'target_role',
        'experience_level', 'profile_completed'
    ]
    list_filter = ['target_role', 'experience_level', 'profile_completed']
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Info', {
            'fields': (
                'phone', 'experience_level', 'target_role',
                'target_companies', 'resume', 'resume_text',
                'skills', 'profile_completed'
            )
        }),
    )