from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from matches.models import (
    Interest,
    get_user_weekly_interest_count,
    get_user_plan_limit
)
from notifications.models import Notification


@login_required
def dashboard_view(request):
    # Interest counts
    interests_received = Interest.objects.filter(
        receiver=request.user
    ).count()

    pending_interests = Interest.objects.filter(
        receiver=request.user,
        status='pending'
    ).count()

    interests_sent = Interest.objects.filter(
        sender=request.user
    ).count()

    # Mutual matches
    accepted_by_them = Interest.objects.filter(
        sender=request.user,
        status='accepted'
    ).values_list('receiver', flat=True)

    accepted_by_me = Interest.objects.filter(
        receiver=request.user,
        status='accepted'
    ).values_list('sender', flat=True)

    mutual_count = len(
        set(accepted_by_them) & set(accepted_by_me)
    )

    # Unread notifications
    unread_notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    # Recent notifications
    recent_notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    # Daily match suggestion (latest one)
    daily_match_notification = Notification.objects.filter(
        user=request.user,
        notification_type='daily_matches',
    ).order_by('-created_at').first()

    # Profile views
    profile_views = 0
    if hasattr(request.user, 'profile'):
        profile_views = request.user.profile.profile_views

    # Weekly interest usage
    used_this_week = get_user_weekly_interest_count(request.user)
    weekly_limit = get_user_plan_limit(request.user)
    remaining_invites = max(0, weekly_limit - used_this_week)

    usage_percent = (
        int((used_this_week / weekly_limit) * 100)
        if weekly_limit > 0 else 0
    )

    return render(request, 'dashboard/index.html', {
        'interests_received': interests_received,
        'pending_interests': pending_interests,
        'interests_sent': interests_sent,
        'mutual_count': mutual_count,
        'unread_notifications': unread_notifications,
        'recent_notifications': recent_notifications,
        'profile_views': profile_views,
        'used_this_week': used_this_week,
        'weekly_limit': weekly_limit,
        'remaining_invites': remaining_invites,
        'usage_percent': usage_percent,
        'daily_match_notification': daily_match_notification,
    })