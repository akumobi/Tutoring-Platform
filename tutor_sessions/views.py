
# Create your views here.
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Session
from .serializers import (
    SessionCreateSerializer,
    SessionListSerializer,
    SessionDetailSerializer
)

# Custom permission: Only students can book sessions
class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class SessionCreateView(generics.CreateAPIView):
    """
    POST /sessions/book/
    Allows a student to book a session with a tutor.
    """
    queryset = Session.objects.all()
    serializer_class = SessionCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)


class UpcomingSessionsView(generics.ListAPIView):
    """
    GET /sessions/upcoming/
    Lists upcoming sessions for the current user (student or tutor).
    """
    serializer_class = SessionListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Session.objects.filter(student=user).order_by('start_time')
        elif user.role == 'tutor':
            return Session.objects.filter(tutor=user).order_by('start_time')
        return Session.objects.none()


class SessionCancelView(generics.DestroyAPIView):
    """
    DELETE /sessions/<id>/cancel/
    Cancels a session (only student or tutor who booked it can cancel).
    """
    queryset = Session.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        session = self.get_object()
        user = request.user
        if session.student != user and session.tutor != user:
            return Response({'detail': 'You do not have permission to cancel this session.'},
                            status=status.HTTP_403_FORBIDDEN)
        session.delete()
        return Response({'detail': 'Session cancelled successfully.'}, status=status.HTTP_204_NO_CONTENT)
