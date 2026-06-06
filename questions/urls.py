from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question-list'),
    path('random/', views.RandomQuestionsView.as_view(), name='random-questions'),
]