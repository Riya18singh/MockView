from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from interviews.models import InterviewSession, Message
from .interview_agent import (
    get_interviewer_response,
    evaluate_answer
)


def get_session_config(session):
    return {
        'interview_type': session.interview_type,
        'difficulty': session.difficulty,
        'target_company': session.target_company,
        'total_questions': session.total_questions,
        'questions_asked': session.questions_asked,
    }


def get_user_profile(user):
    return {
        'experience_level': user.experience_level,
        'target_role': user.target_role,
        'skills': user.skills or [],
        'resume_text': user.resume_text or '',
    }


def get_conversation_history(session):
    messages = session.messages.all().order_by('timestamp')
    history = []
    for msg in messages:
        if msg.role in ['interviewer', 'candidate']:
            history.append({
                'role': msg.role,
                'content': msg.content
            })
    return history


class StartInterviewView(APIView):
    """
    Called when user starts interview.
    AI sends first message/introduction.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        session = get_object_or_404(
            InterviewSession,
            id=session_id,
            user=request.user
        )

        if session.status != 'ongoing':
            return Response(
                {'error': 'Session must be started first'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if already has messages
        if session.messages.exists():
            return Response(
                {'error': 'Interview already started'},
                status=status.HTTP_400_BAD_REQUEST
            )

        session_config = get_session_config(session)
        user_profile = get_user_profile(request.user)

        # Get opening message from AI
        opening_message = get_interviewer_response(
            session_config=session_config,
            user_profile=user_profile,
            conversation_history=[],
            last_score=None
        )

        # Save AI message to DB
        Message.objects.create(
            session=session,
            role='interviewer',
            content=opening_message
        )

        return Response({
            'message': opening_message,
            'questions_asked': session.questions_asked,
            'total_questions': session.total_questions,
        })


class SendMessageView(APIView):
    """
    Candidate sends answer.
    1. Save candidate message
    2. Evaluate the answer
    3. Get next question from AI
    4. Save AI message
    5. Return everything
    """
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

        candidate_message = request.data.get('message', '').strip()

        if not candidate_message:
            return Response(
                {'error': 'Message cannot be empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check interview not finished
        if session.questions_asked >= session.total_questions:
            return Response(
                {'error': 'Interview is complete'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get last interviewer question
        last_question = session.messages.filter(
            role='interviewer'
        ).last()

        # Evaluate candidate answer
        evaluation = None
        if last_question:
            evaluation = evaluate_answer(
                question=last_question.content,
                answer=candidate_message,
                interview_type=session.interview_type,
                difficulty=session.difficulty
            )

        # Save candidate message with score
        candidate_msg = Message.objects.create(
            session=session,
            role='candidate',
            content=candidate_message,
            score=evaluation['score'] if evaluation else None,
            feedback=evaluation['feedback'] if evaluation else None
        )

        # Update question count
        session.questions_asked += 1
        session.save()

        # Get next question from AI
        session_config = get_session_config(session)
        user_profile = get_user_profile(request.user)
        conversation_history = get_conversation_history(session)

        last_score = evaluation['score'] if evaluation else None

        next_question = get_interviewer_response(
            session_config=session_config,
            user_profile=user_profile,
            conversation_history=conversation_history,
            last_score=last_score
        )

        # Save AI response
        Message.objects.create(
            session=session,
            role='interviewer',
            content=next_question
        )

        return Response({
            'your_answer_score': evaluation['score'] if evaluation else None,
            'feedback': evaluation['feedback'] if evaluation else None,
            'strong_points': evaluation['strong_points'] if evaluation else None,
            'weak_points': evaluation['weak_points'] if evaluation else None,
            'next_question': next_question,
            'questions_asked': session.questions_asked,
            'total_questions': session.total_questions,
            'interview_complete': session.questions_asked >= session.total_questions
        })