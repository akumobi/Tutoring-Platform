
# Create your views here.
from rest_framework import generics, permissions
from .models import TutorProfile
from .serializers import TutorProfileSerializer

class TutorProfileListView(generics.ListAPIView):
    """
    Public list of approved tutors.
    """
    queryset = TutorProfile.objects.filter(is_approved=True)
    serializer_class = TutorProfileSerializer
    permission_classes = [permissions.AllowAny]

class ApplyAsTutorView(generics.CreateAPIView):
    """
    Tutor submits an application for a profile.
    """
    serializer_class = TutorProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ApproveTutorView(generics.UpdateAPIView):
    """
    Admin approves a tutor by updating the `is_approved` field.
    """
    queryset = TutorProfile.objects.all()
    serializer_class = TutorProfileSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(is_approved=True)