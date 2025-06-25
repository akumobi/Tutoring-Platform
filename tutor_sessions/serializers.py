from rest_framework import serializers
from .models import Session

class SessionCreateSerializer(serializers.ModelSerializer):
    """
    Used by a student to book a session with a tutor.
    Fields required: tutor, start_time, end_time.
    The student field will be set automatically from request.user.
    """

    class Meta:
        model = Session
        fields = ['id', 'tutor', 'start_time', 'end_time']

    def create(self, validated_data):
        # Automatically assign the logged-in user as the student
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)


class SessionListSerializer(serializers.ModelSerializer):
    """
    Lists upcoming sessions for students and tutors.
    Includes basic session info with readable tutor/student names.
    """

    tutor_name = serializers.CharField(source='tutor.username', read_only=True)
    student_name = serializers.CharField(source='student.username', read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'tutor_name', 'student_name', 'start_time', 'end_time', 'status']


class SessionDetailSerializer(serializers.ModelSerializer):
    
    # Shows full details of a session and allows updates (e.g., cancel).

    class Meta:
        model = Session
        fields = '__all__'
        read_only_fields = ['student']  # Prevent changing the student manually
