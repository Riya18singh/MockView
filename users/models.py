from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    EXPERIENCE_CHOICES = [
        ('fresher', 'Fresher'),
        ('junior', 'Junior (1-2 years)'),
        ('mid', 'Mid (2-4 years)'),
        ('senior', 'Senior (4+ years)'),
    ]

    TARGET_ROLE_CHOICES = [
        ('sde', 'Software Developer Engineer'),
        ('ml_engineer', 'ML Engineer'),
        ('data_scientist', 'Data Scientist'),
        ('frontend', 'Frontend Developer'),
        ('backend', 'Backend Developer'),
        ('fullstack', 'Fullstack Developer'),
        ('devops', 'DevOps Engineer'),
    ]

    # Extra fields
    phone = models.CharField(max_length=15, blank=True, null=True)
    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default='fresher'
    )
    target_role = models.CharField(
        max_length=20,
        choices=TARGET_ROLE_CHOICES,
        default='sde'
    )
    target_companies = models.JSONField(default=list, blank=True)
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )
    resume_text = models.TextField(blank=True, null=True)
    skills = models.JSONField(default=list, blank=True)
    profile_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} - {self.target_role}"