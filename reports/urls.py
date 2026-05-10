from django.urls import path
from . import views

urlpatterns = [
    path(
        'sessions/<int:session_id>/generate/',
        views.GenerateReportView.as_view(),
        name='generate-report'
    ),
    path(
        'sessions/<int:session_id>/',
        views.GetReportView.as_view(),
        name='get-report'
    ),
    path(
        'all/',
        views.AllReportsView.as_view(),
        name='all-reports'
    ),
    path(
        'progress/',
        views.UserProgressView.as_view(),
        name='user-progress'
    ),
]