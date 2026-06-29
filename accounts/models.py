from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    phone = models.CharField(
        max_length=15, unique=True
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        null=True,
        blank=True
    )
    is_verified = models.BooleanField(default=False)
    is_profile_complete = models.BooleanField(default=False)

    # OTP Fields
    otp_code = models.CharField(
        max_length=6, blank=True, null=True
    )
    otp_created_at = models.DateTimeField(
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.phone})"

    def is_otp_valid(self, otp):
        """Check if OTP is valid and not expired"""
        if not self.otp_code or not self.otp_created_at:
            return False
        # OTP valid for 10 minutes
        expiry = self.otp_created_at + timezone.timedelta(
            minutes=10
        )
        return (
            self.otp_code == otp and
            timezone.now() < expiry
        )


class AccountDeletionRequest(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='deletion_requests'
    )
    reason = models.TextField(
        blank=True, null=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_deletion_requests'
    )
    admin_note = models.CharField(
        max_length=255, blank=True, null=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.status}"