from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import InterviewSession, Message
from .serializers import (
    InterviewSessionSerializer,
    CreateSessionSerializer,
    MessageSerializer
)


class CreateSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateSessionSerializer(data=request.data)
        if serializer.is_valid():
            session = serializer.save(user=request.user)
            return Response({
                'message': 'Interview session created',
                'session': InterviewSessionSerializer(session).data
            }, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SessionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sessions = InterviewSession.objects.filter(
            user=request.user
        )
        serializer = InterviewSessionSerializer(
            sessions, many=True
        )
        return Response({
            'total_sessions': sessions.count(),
            'sessions': serializer.data
        })


class SessionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        session = get_object_or_404(
            InterviewSession,
            id=session_id,
            user=request.user
        )
        serializer = InterviewSessionSerializer(session)
        return Response(serializer.data)

    def delete(self, request, session_id):
        session = get_object_or_404(
            InterviewSession,
            id=session_id,
            user=request.user
        )
        session.delete()
        return Response({
            'message': 'Session deleted successfully'
        }, status=status.HTTP_200_OK)


class StartSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        session = get_object_or_404(
            InterviewSession,
            id=session_id,
            user=request.user
        )

        if session.status != 'pending':
            return Response(
                {'error': f'Session is already {session.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        session.status = 'ongoing'
        session.save()

        return Response({
            'message': 'Interview started',
            'session_id': session.id,
            'interview_type': session.interview_type,
            'difficulty': session.difficulty,
            'target_company': session.target_company,
            'total_questions': session.total_questions,
        })


class EndSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        session = get_object_or_404(
            InterviewSession,
            id=session_id,
            user=request.user
        )

        if session.status != 'ongoing':
            return Response(
                {'error': 'Session is not ongoing'},
                status=status.HTTP_400_BAD_REQUEST
            )

        session.status = 'completed'
        session.ended_at = timezone.now()
        session.save()

        return Response({
            'message': 'Interview ended successfully',
            'session_id': session.id,
            'status': session.status,
        })


class SessionMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        session = get_object_or_404(
            InterviewSession,
            id=session_id,
            user=request.user
        )
        messages = session.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response({
            'session_id': session_id,
            'total_messages': messages.count(),
            'messages': serializer.data
        })