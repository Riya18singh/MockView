from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from interviews.models import InterviewSession
from .models import EvaluationReport, UserProgress
from agents.report_agent import generate_report


class GenerateReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):
        session = get_object_or_404(
            InterviewSession,
            id=session_id,
            user=request.user
        )

        if session.status != 'completed':
            return Response(
                {'error': 'Session must be completed first'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if report already exists
        if hasattr(session, 'report'):
            return Response(
                {'error': 'Report already generated'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate report
        report_data = generate_report(session)

        if not report_data:
            return Response(
                {'error': 'No messages found in session'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save report
        report = EvaluationReport.objects.create(
            session=session,
            user=request.user,
            overall_score=report_data['overall_score'],
            technical_score=report_data['technical_score'],
            communication_score=report_data['communication_score'],
            strong_topics=report_data['strong_topics'],
            weak_topics=report_data['weak_topics'],
            detailed_feedback=report_data['overall_feedback'],
            improvement_tips=report_data['improvement_tips'],
            question_breakdown=report_data['question_breakdown'],
            total_questions_asked=report_data['total_questions_asked'],
            average_score=report_data['average_score']
        )

        # Update session score
        session.overall_score = report_data['overall_score']
        session.save()

        # Update user progress
        update_user_progress(request.user, report)

        return Response({
            'message': 'Report generated successfully',
            'report': format_report(report)
        })


class GetReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id):
        session = get_object_or_404(
            InterviewSession,
            id=session_id,
            user=request.user
        )

        if not hasattr(session, 'report'):
            return Response(
                {'error': 'Report not generated yet'},
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(format_report(session.report))


class AllReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reports = EvaluationReport.objects.filter(
            user=request.user
        )

        return Response({
            'total_reports': reports.count(),
            'reports': [format_report(r) for r in reports]
        })


class UserProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            progress = request.user.progress
            return Response({
                'total_interviews': progress.total_interviews,
                'average_score': progress.average_score,
                'best_score': progress.best_score,
                'weak_topics': progress.weak_topics,
                'strong_topics': progress.strong_topics,
                'scores_history': progress.scores_history,
            })
        except UserProgress.DoesNotExist:
            return Response({
                'total_interviews': 0,
                'average_score': 0,
                'best_score': 0,
                'weak_topics': [],
                'strong_topics': [],
                'scores_history': [],
            })


def format_report(report):
    return {
        'id': report.id,
        'session_id': report.session.id,
        'overall_score': report.overall_score,
        'technical_score': report.technical_score,
        'communication_score': report.communication_score,
        'average_score': report.average_score,
        'strong_topics': report.strong_topics,
        'weak_topics': report.weak_topics,
        'detailed_feedback': report.detailed_feedback,
        'improvement_tips': report.improvement_tips,
        'question_breakdown': report.question_breakdown,
        'total_questions_asked': report.total_questions_asked,
        'generated_at': report.generated_at,
    }


def update_user_progress(user, report):
    progress, created = UserProgress.objects.get_or_create(
        user=user
    )

    progress.total_interviews += 1
    progress.scores_history.append(report.overall_score)

    # Update average
    progress.average_score = round(
        sum(progress.scores_history) / len(progress.scores_history), 1
    )

    # Update best score
    if report.overall_score > progress.best_score:
        progress.best_score = report.overall_score

    # Update weak topics
    for topic in report.weak_topics:
        if topic not in progress.weak_topics:
            progress.weak_topics.append(topic)

    # Update strong topics
    for topic in report.strong_topics:
        if topic not in progress.strong_topics:
            progress.strong_topics.append(topic)

    progress.save()