from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from rest_framework_simplejwt.tokens import AccessToken

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
            return Response({'message': 'Session created', 'session': InterviewSessionSerializer(session).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SessionListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        sessions = InterviewSession.objects.filter(user=request.user)
        serializer = InterviewSessionSerializer(sessions, many=True)
        return Response({'total_sessions': sessions.count(), 'sessions': serializer.data})

class SessionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, session_id):
        session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
        return Response(InterviewSessionSerializer(session).data)

class StartSessionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, session_id):
        session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
        session.status = 'ongoing'
        session.save()
        return Response({'message': 'Interview started', 'session_id': session.id})

class EndSessionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, session_id):
        session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
        session.status = 'completed'
        session.ended_at = timezone.now()
        session.save()
        return Response({'message': 'Interview ended', 'session_id': session.id})

class SessionMessagesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, session_id):
        session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
        serializer = MessageSerializer(session.messages.all(), many=True)
        return Response({'messages': serializer.data})

def room_view(request, session_id):
    # This renders the chat room HTML
    session = get_object_or_404(InterviewSession, id=session_id)
    token = str(AccessToken.for_user(session.user))
    return render(request, 'interview_room.html', {'session_id': session.id, 'access_token': token})