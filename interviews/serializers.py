from rest_framework import serializers
from .models import InterviewSession, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            'id', 'role', 'content',
            'score', 'feedback', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']


class InterviewSessionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    duration_minutes = serializers.SerializerMethodField()

    class Meta:
        model = InterviewSession
        fields = [
            'id', 'interview_type', 'difficulty',
            'target_company', 'total_questions',
            'questions_asked', 'status', 'started_at',
            'ended_at', 'overall_score', 'summary',
            'messages', 'duration_minutes'
        ]
        read_only_fields = [
            'id', 'started_at', 'ended_at',
            'overall_score', 'summary',
            'questions_asked', 'status'
        ]

    def get_duration_minutes(self, obj):
        if obj.ended_at and obj.started_at:
            delta = obj.ended_at - obj.started_at
            return round(delta.total_seconds() / 60, 1)
        return None


class CreateSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewSession
        fields = [
            'interview_type', 'difficulty',
            'target_company', 'total_questions'
        ]