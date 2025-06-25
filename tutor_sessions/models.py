
# Create your models here.
from django.db import models
from django.conf import settings
from tutors.models import TutorProfile

class Session(models.Model):
    
    # Model representing a tutoring session between a student and a tutor.
    
    tutor = models.ForeignKey(
        TutorProfile,
        on_delete=models.CASCADE,
        related_name='sessions',
        help_text="The tutor conducting the session"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_sessions',
        help_text="The student booking the session"
    )
    start_time = models.DateTimeField(
        help_text="Start time of the session"
    )
    end_time = models.DateTimeField(
        help_text="End time of the session"
    )
    topic = models.CharField(
        max_length=200,
        help_text="Topic or focus area of the session"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending',
        help_text="Current status of the session"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.topic} - {self.student} with {self.tutor.user} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"
