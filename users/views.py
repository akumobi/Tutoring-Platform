from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Use the custom user model
User = get_user_model()

# Custom JWT serializer that includes extra user info in the token response
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Run default validation to get the access and refresh tokens
        data = super().validate(attrs)

        # Add extra fields to the response
        data.update({
            'user_id': self.user.id,
            'username': self.user.username,
            'role': self.user.role,
            'is_approved': self.user.is_approved,
        })
        return data


# Custom login view using the custom JWT serializer
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# Registration view using the RegisterSerializer
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]  # Anyone can register
    serializer_class = RegisterSerializer


# Profile view to return the authenticated user's data
class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be logged in

    # Return the currently logged-in user
    def get_object(self):
        return self.request.user
