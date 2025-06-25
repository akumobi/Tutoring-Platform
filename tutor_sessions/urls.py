from django.urls import path
from .views import SessionCreateView, UpcomingSessionsView, SessionCancelView

urlpatterns = [
    path('book/', SessionCreateView.as_view(), name='session-book'),
    path('upcoming/', UpcomingSessionsView.as_view(), name='session-upcoming'),
    path('<int:pk>/cancel/', SessionCancelView.as_view(), name='session-cancel'),
]
