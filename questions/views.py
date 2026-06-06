from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Question
from .serializers import QuestionSerializer


class QuestionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        category = request.query_params.get('category')
        difficulty = request.query_params.get('difficulty')
        company = request.query_params.get('company')

        questions = Question.objects.all()

        if category:
            questions = questions.filter(category=category)
        if difficulty:
            questions = questions.filter(difficulty=difficulty)
        if company:
            questions = questions.filter(company=company)

        serializer = QuestionSerializer(questions, many=True)
        return Response({
            'total': questions.count(),
            'questions': serializer.data
        })


class RandomQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        category = request.query_params.get('category', 'dsa')
        difficulty = request.query_params.get('difficulty', 'medium')
        company = request.query_params.get('company', 'general')
        count = int(request.query_params.get('count', 5))

        questions = Question.objects.filter(
            category=category,
            difficulty=difficulty,
        )

        if company != 'general':
            questions = questions.filter(company=company)

        questions = questions.order_by('?')[:count]

        serializer = QuestionSerializer(questions, many=True)
        return Response({
            'total': len(serializer.data),
            'questions': serializer.data
        })