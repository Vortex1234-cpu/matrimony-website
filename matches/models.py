from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Interest(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='interests_sent'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='interests_received'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    message = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"


def get_user_weekly_interest_count(user):
    """Count interests sent this week"""
    week_start = timezone.now() - timedelta(days=7)
    return Interest.objects.filter(
        sender=user,
        sent_at__gte=week_start
    ).count()


def get_user_plan_limit(user):
    """Get weekly interest limit based on plan"""
    from payments.models import Subscription
    from django.utils import timezone

    active_sub = Subscription.objects.filter(
        user=user,
        status='active',
        end_date__gt=timezone.now()
    ).select_related('plan').first()

    if active_sub:
        return active_sub.plan.max_interests_per_week
    return 3  # Free plan default


def can_send_interest(user):
    """Check if user can send more interests"""
    limit = get_user_plan_limit(user)
    used = get_user_weekly_interest_count(user)
    return used < limit, used, limit