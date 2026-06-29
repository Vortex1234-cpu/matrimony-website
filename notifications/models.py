from django.db import models
from django.conf import settings


class Notification(models.Model):

    TYPE_CHOICES = [
        ('interest_received', 'Interest Received'),
        ('interest_accepted', 'Interest Accepted'),
        ('interest_rejected', 'Interest Rejected'),
        ('profile_approved', 'Profile Approved'),
        ('profile_rejected', 'Profile Rejected'),
        ('new_match', 'New Match'),
        ('subscription', 'Subscription'),
        ('daily_matches', 'Daily Match Suggestions'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES
    )
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.phone} - {self.title}"


class DeviceToken(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="device_tokens",
        null=True,
        blank=True
    )
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.token[:30]