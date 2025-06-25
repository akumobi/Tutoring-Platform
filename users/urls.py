from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, ProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Register a new user
    path('register/', RegisterView.as_view(), name='auth-register'),
    
    # Login and receive JWT access and refresh tokens
    path('login/', CustomTokenObtainPairView.as_view(), name='auth-login'),
    
    # View the logged-in user's profile
    path('profile/', ProfileView.as_view(), name='auth-profile'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

