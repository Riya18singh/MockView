from rest_framework import serializers
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'id', 'question_text', 'category',
            'difficulty', 'company', 'model_answer',
            'tags', 'times_asked'
        ]