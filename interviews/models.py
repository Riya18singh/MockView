from django.db import models
from django.conf import settings


class InterviewSession(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
    ]

    INTERVIEW_TYPE_CHOICES = [
        ('dsa', 'Data Structures & Algorithms'),
        ('system_design', 'System Design'),
        ('hr', 'HR & Behavioural'),
        ('core_cs', 'Core CS (OS, DBMS, Networks)'),
        ('mixed', 'Mixed'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    COMPANY_CHOICES = [
        ('google', 'Google'),
        ('microsoft', 'Microsoft'),
        ('amazon', 'Amazon'),
        ('flipkart', 'Flipkart'),
        ('zomato', 'Zomato'),
        ('razorpay', 'Razorpay'),
        ('tcs', 'TCS'),
        ('infosys', 'Infosys'),
        ('wipro', 'Wipro'),
        ('startup', 'Generic Startup'),
        ('general', 'General'),
    ]

    # Link to user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sessions'
    )

    # Interview config
    interview_type = models.CharField(
        max_length=20,
        choices=INTERVIEW_TYPE_CHOICES,
        default='mixed'
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium'
    )
    target_company = models.CharField(
        max_length=20,
        choices=COMPANY_CHOICES,
        default='general'
    )
    total_questions = models.IntegerField(default=10)
    questions_asked = models.IntegerField(default=0)

    # Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # Timestamps
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    # Summary (filled after completion)
    overall_score = models.FloatField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.username} - {self.interview_type} - {self.status}"


class Message(models.Model):

    ROLE_CHOICES = [
        ('interviewer', 'Interviewer'),
        ('candidate', 'Candidate'),
        ('system', 'System'),
    ]

    session = models.ForeignKey(
        InterviewSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )
    content = models.TextField()
    
    # Evaluation of candidate answer
    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.session} - {self.role} - {self.timestamp}"