from django.db import models


class Question(models.Model):

    CATEGORY_CHOICES = [
        ('dsa', 'Data Structures & Algorithms'),
        ('system_design', 'System Design'),
        ('hr', 'HR & Behavioural'),
        ('core_cs', 'Core CS'),
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

    question_text = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES
    )
    company = models.CharField(
        max_length=20,
        choices=COMPANY_CHOICES,
        default='general'
    )
    model_answer = models.TextField(blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)
    times_asked = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'difficulty']

    def __str__(self):
        return f"{self.category} - {self.difficulty} - {self.question_text[:50]}"