from django.db import models
from django.conf import settings
from django.utils import timezone


class Plan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )
    duration_days = models.IntegerField(default=30)
    can_send_interest = models.BooleanField(default=True)
    can_view_contact = models.BooleanField(default=False)
    can_message = models.BooleanField(default=False)
    max_interests_per_week = models.IntegerField(default=3)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.SET_NULL, null=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    start_date = models.DateTimeField(
        default=timezone.now
    )
    end_date = models.DateTimeField()
    razorpay_order_id = models.CharField(
        max_length=100, blank=True, null=True
    )
    razorpay_payment_id = models.CharField(
        max_length=100, blank=True, null=True
    )
    razorpay_signature = models.CharField(
        max_length=200, blank=True, null=True
    )
    amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.plan.name}'

    @property
    def is_active(self):
        return (
            self.status == 'active'
            and self.end_date > timezone.now()
        )