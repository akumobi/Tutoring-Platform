from rest_framework import serializers
from .models import TutorProfile

class TutorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorProfile
        fields = '__all__'
        read_only_fields = ['user', 'is_approved', 'created_at']