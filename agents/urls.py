from django.urls import path
from . import views

urlpatterns = [
    path(
        'sessions/<int:session_id>/begin/',
        views.StartInterviewView.as_view(),
        name='begin-interview'
    ),
    path(
        'sessions/<int:session_id>/chat/',
        views.SendMessageView.as_view(),
        name='send-message'
    ),
    path(
        'resume/parse/',
        views.ParseResumeView.as_view(),
        name='parse-resume'
    ),
]