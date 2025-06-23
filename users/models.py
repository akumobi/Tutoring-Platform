# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Adds role-based access and additional fields for the tutoring platform.
    """

    # Define possible roles for the user: student, tutor, or admin
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('tutor', 'Tutor'),
        ('admin', 'Admin'),
    ]

    # Role determines the user's permissions and view access across the app
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student',
        help_text="Defines the user's role in the system (student, tutor, admin)."
    )

    # Optional phone number field for user profile/contact purposes
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="User's phone number for contact or verification."
    )

    # Tutor approval flag: Admin must approve tutors before they can appear public or take sessions
    is_approved = models.BooleanField(
        default=False,
        help_text="For tutors: Indicates whether the user has been approved by an admin."
    )

    def __str__(self):
    # String representation of the user, showing username and role.
        return f"{self.username} ({self.role})"
