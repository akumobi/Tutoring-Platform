
# Create your models here.

from django.db import models
from django.conf import settings

class TutorProfile(models.Model):
    """
    Represents a tutor's profile.
    Linked to the User model via a one-to-one relationship.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tutor_profile')

    # Short bio or introduction
    bio = models.TextField()

    # Comma-separated list of subjects the tutor teaches
    subjects_taught = models.CharField(max_length=255)

    # Tutor's hourly rate (in your currency unit)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)

    # Weekly availability in text format (e.g., JSON or time ranges)
    availability = models.TextField()

    # Whether the tutor has been approved by an admin
    is_approved = models.BooleanField(default=False)

    # Timestamp for tracking
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TutorProfile: {self.user.username}"
