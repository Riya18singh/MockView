from django.db import models
from django.conf import settings


class EvaluationReport(models.Model):

    session = models.OneToOneField(
        'interviews.InterviewSession',
        on_delete=models.CASCADE,
        related_name='report'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports'
    )

    # Scores
    overall_score = models.FloatField(default=0)
    technical_score = models.FloatField(default=0)
    communication_score = models.FloatField(default=0)

    # Analysis
    strong_topics = models.JSONField(default=list)
    weak_topics = models.JSONField(default=list)
    detailed_feedback = models.TextField(blank=True)
    improvement_tips = models.JSONField(default=list)

    # Question wise breakdown
    question_breakdown = models.JSONField(default=list)

    # Meta
    total_questions_asked = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"Report - {self.user.username} - {self.overall_score}"


class UserProgress(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress'
    )

    total_interviews = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)
    best_score = models.FloatField(default=0)
    weak_topics = models.JSONField(default=list)
    strong_topics = models.JSONField(default=list)
    scores_history = models.JSONField(default=list)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Progress - {self.user.username}"