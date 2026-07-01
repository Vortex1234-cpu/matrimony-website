from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
import threading
from .models import (
    Interest,
    can_send_interest,
    get_user_weekly_interest_count,
    get_user_plan_limit
)
from accounts.models import User
from accounts.email_utils import (
    send_interest_received_email,
    send_interest_accepted_email
)
from profiles.models import Profile
from notifications.services import send_push_notification


@login_required
def send_interest(request, profile_id):
    if request.method != 'POST':
        return HttpResponse(status=405)

    receiver_profile = get_object_or_404(Profile, id=profile_id)
    receiver = receiver_profile.user

    # Prevent sending to yourself
    if receiver == request.user:
        if request.headers.get('HX-Request'):
            return HttpResponse(
                '<span class="badge-rejected">'
                '⚠️ Cannot send to yourself'
                '</span>'
            )
        return redirect('search')

    # Check weekly limit
    allowed, used, limit = can_send_interest(request.user)

    if not allowed:
        if request.headers.get('HX-Request'):
            return HttpResponse(f'''
            <div class="limit-warning-box">
                <div class="limit-icon">🚫</div>
                <div class="limit-text">
                    <strong>Weekly Limit Reached!</strong><br>
                    <span>You have used {used}/{limit} interests
                    this week.</span><br>
                    <a href="/payments/plans/"
                       class="limit-upgrade-btn">
                        ⚡ Upgrade Plan
                    </a>
                </div>
            </div>
            ''')
        messages.error(
            request,
            f'🚫 Weekly limit reached! You have used {used}/{limit} interests. Upgrade your plan.'
        )
        return redirect('plans_page')

    # Check if already sent
    existing = Interest.objects.filter(
        sender=request.user,
        receiver=receiver
    ).first()

    if existing:
        if request.headers.get('HX-Request'):
            if existing.status == 'pending':
                return HttpResponse(
                    '<span class="badge-pending">'
                    '⏳ Already Sent'
                    '</span>'
                )
            elif existing.status == 'accepted':
                return HttpResponse(
                    '<span class="badge-accepted">'
                    '✅ Interest Accepted'
                    '</span>'
                )
        return redirect('search')

    # Create interest
    Interest.objects.create(
        sender=request.user,
        receiver=receiver,
        status='pending'
    )

    # Notify receiver in DB
    from notifications.models import Notification
    Notification.objects.create(
        user=receiver,
        notification_type='interest_received',
        title='New Interest Received! 💌',
        message=f'{request.user.first_name} sent you an interest.',
        link=f'/profiles/{profile_id}/'
    )

    # Send email + push notification in background thread (non-blocking)
    def send_notifications_async():
        try:
            send_interest_received_email(receiver, request.user)
        except Exception:
            pass
        try:
            send_push_notification(
                user=receiver,
                title='New Interest Received! 💌',
                body=f'{request.user.first_name} sent you an interest.',
                data={
                    'type': 'interest_received',
                    'profile_id': str(profile_id)
                }
            )
        except Exception:
            pass

    threading.Thread(target=send_notifications_async, daemon=True).start()

    # Recalculate after sending
    new_used = get_user_weekly_interest_count(request.user)
    new_limit = get_user_plan_limit(request.user)
    remaining = new_limit - new_used

    if request.headers.get('HX-Request'):
        remaining_html = ''
        if new_limit <= 3:  # Free plan
            remaining_html = f'''
            <small style="color:var(--primary);
                          font-size:0.72rem;
                          display:block;margin-top:4px;">
                {remaining} invites left this week
            </small>
            '''
        return HttpResponse(f'''
        <div>
            <span class="badge-accepted">
                ✅ Interest Sent!
            </span>
            {remaining_html}
        </div>
        ''')

    messages.success(request, '💌 Interest sent!')
    return redirect('search')


@login_required
def accept_interest(request, interest_id):
    interest = get_object_or_404(
        Interest,
        id=interest_id,
        receiver=request.user
    )
    interest.status = 'accepted'
    interest.save()

    from notifications.models import Notification
    Notification.objects.create(
        user=interest.sender,
        notification_type='interest_accepted',
        title='Interest Accepted! 🎉',
        message=f'{request.user.first_name} accepted your interest!',
        link=f'/profiles/{interest.receiver.profile.id}/'
    )

    # Send email + push notification in background thread (non-blocking)
    def send_notifications_async():
        try:
            send_interest_accepted_email(interest.sender, request.user)
        except Exception:
            pass
        try:
            send_push_notification(
                user=interest.sender,
                title='Interest Accepted! 🎉',
                body=f'{request.user.first_name} accepted your interest!',
                data={
                    'type': 'interest_accepted',
                    'profile_id': str(interest.receiver.profile.id)
                }
            )
        except Exception:
            pass

    threading.Thread(target=send_notifications_async, daemon=True).start()

    if request.headers.get('HX-Request'):
        return HttpResponse(f'''
        <div class="interest-card"
             id="interest-card-{interest.id}"
             style="opacity:0.75;">
            <div class="d-flex align-items-center
                        justify-content-between p-2">
                <span class="text-muted small">
                    Interest from
                    <strong>{interest.sender.first_name}</strong>
                </span>
                <span class="badge-accepted">✅ Accepted</span>
            </div>
        </div>
        ''')

    messages.success(request, '✅ Interest accepted!')
    return redirect('interests_received')


@login_required
def reject_interest(request, interest_id):
    interest = get_object_or_404(
        Interest,
        id=interest_id,
        receiver=request.user
    )
    interest.status = 'rejected'
    interest.save()

    if request.headers.get('HX-Request'):
        return HttpResponse('')

    messages.success(request, 'Interest rejected.')
    return redirect('interests_received')


@login_required
def interests_received(request):
    interests = Interest.objects.filter(
        receiver=request.user
    ).select_related(
        'sender__profile'
    ).order_by('-sent_at')

    pending_count = interests.filter(status='pending').count()
    accepted_count = interests.filter(status='accepted').count()

    status_filter = request.GET.get('status', '')
    if status_filter:
        interests = interests.filter(status=status_filter)

    return render(request, 'matches/interests_received.html', {
        'interests': interests,
        'pending_count': pending_count,
        'accepted_count': accepted_count,
        'status_filter': status_filter,
    })


@login_required
def interests_sent(request):
    interests = Interest.objects.filter(
        sender=request.user
    ).select_related(
        'receiver__profile'
    ).order_by('-sent_at')

    status_filter = request.GET.get('status', '')
    if status_filter:
        interests = interests.filter(status=status_filter)

    used = get_user_weekly_interest_count(request.user)
    limit = get_user_plan_limit(request.user)

    return render(request, 'matches/interests_sent.html', {
        'interests': interests,
        'status_filter': status_filter,
        'used': used,
        'limit': limit,
        'remaining': limit - used,
    })


@login_required
def mutual_matches(request):
    accepted_by_them = Interest.objects.filter(
        sender=request.user,
        status='accepted'
    ).values_list('receiver', flat=True)

    accepted_by_me = Interest.objects.filter(
        receiver=request.user,
        status='accepted'
    ).values_list('sender', flat=True)

    mutual_ids = set(accepted_by_them) & set(accepted_by_me)
    mutual_profiles = Profile.objects.filter(
        user__id__in=mutual_ids,
        is_approved=True
    )

    return render(request, 'matches/mutual_matches.html', {
        'profiles': mutual_profiles
    })