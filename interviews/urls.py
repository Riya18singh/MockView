from django.urls import path
from . import views

urlpatterns = [
    # Session management
    path('sessions/', views.SessionListView.as_view(), name='session-list'),
    path('sessions/create/', views.CreateSessionView.as_view(), name='create-session'),
    path('sessions/<int:session_id>/', views.SessionDetailView.as_view(), name='session-detail'),
    path('sessions/<int:session_id>/start/', views.StartSessionView.as_view(), name='start-session'),
    path('sessions/<int:session_id>/end/', views.EndSessionView.as_view(), name='end-session'),
    path('sessions/<int:session_id>/messages/', views.SessionMessagesView.as_view(), name='session-messages'),
    
    # NEW: The Web UI for the Interview Room
    path('room/<int:session_id>/', views.room_view, name='room'),
]