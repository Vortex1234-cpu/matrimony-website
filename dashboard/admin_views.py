from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from profiles.models import Profile
from accounts.models import User
from matches.models import Interest
from notifications.models import Notification
import threading


def is_admin(user):
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    try:
        total_profiles = Profile.objects.count()
        pending_profiles = Profile.objects.filter(
            is_approved=False
        ).count()
        approved_profiles = Profile.objects.filter(
            is_approved=True
        ).count()
        total_users = User.objects.count()
        total_interests = Interest.objects.count()
        accepted_interests = Interest.objects.filter(
            status='accepted'
        ).count()
        recent_profiles = Profile.objects.order_by(
            '-created_at'
        )[:5]

        return render(request, 'admin_panel/dashboard.html', {
            'total_profiles': total_profiles,
            'pending_profiles': pending_profiles,
            'approved_profiles': approved_profiles,
            'total_users': total_users,
            'total_interests': total_interests,
            'accepted_interests': accepted_interests,
            'recent_profiles': recent_profiles,
        })
    except Exception as e:
        messages.error(request, f'Dashboard error: {str(e)}')
        return redirect('dashboard')


@login_required
@user_passes_test(is_admin)
def admin_profiles(request):
    try:
        status = request.GET.get('status', 'pending')

        if status == 'pending':
            profiles = Profile.objects.filter(
                is_approved=False
            ).select_related('user').order_by('-created_at')
        elif status == 'approved':
            profiles = Profile.objects.filter(
                is_approved=True
            ).select_related('user').order_by('-created_at')
        else:
            profiles = Profile.objects.all().select_related(
                'user'
            ).order_by('-created_at')

        pending_count = Profile.objects.filter(
            is_approved=False
        ).count()
        approved_count = Profile.objects.filter(
            is_approved=True
        ).count()

        return render(request, 'admin_panel/profiles.html', {
            'profiles': profiles,
            'status': status,
            'pending_count': pending_count,
            'approved_count': approved_count,
        })
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('admin_dashboard')


@login_required
@user_passes_test(is_admin)
def approve_profile(request, profile_id):
    try:
        profile = get_object_or_404(Profile, id=profile_id)

        # Approve profile
        profile.is_approved = True
        profile.save()

        # Notify user in DB
        try:
            Notification.objects.create(
                user=profile.user,
                notification_type='profile_approved',
                title='🎉 Profile Approved!',
                message='Your profile is now live and visible to matches.',
                link='/profiles/me/'
            )
        except Exception as e:
            print(f'Notification error: {e}')

        # Send email in background thread (non-blocking)
        try:
            from accounts.email_utils import (
                send_profile_approved_email
            )
            user_ref = profile.user

            def send_email_bg():
                try:
                    send_profile_approved_email(user_ref)
                except Exception as e:
                    print(f'Email error: {e}')

            t = threading.Thread(
                target=send_email_bg,
                daemon=True
            )
            t.start()
        except Exception as e:
            print(f'Email thread error: {e}')

        messages.success(
            request,
            f'✅ {profile.full_name} profile approved!'
        )

    except Exception as e:
        messages.error(
            request,
            f'❌ Error approving profile: {str(e)}'
        )

    return redirect('admin_profiles')


@login_required
@user_passes_test(is_admin)
def reject_profile(request, profile_id):
    try:
        profile = get_object_or_404(Profile, id=profile_id)
        user_name = profile.full_name

        # Notify user in DB
        try:
            Notification.objects.create(
                user=profile.user,
                notification_type='profile_rejected',
                title='❌ Profile Needs Update',
                message='Your profile was not approved. Please update your details and resubmit.',
                link='/profiles/edit/'
            )
        except Exception as e:
            print(f'Notification error: {e}')

        # Delete profile
        profile.delete()

        messages.warning(
            request,
            f'Profile of {user_name} rejected and removed.'
        )

    except Exception as e:
        messages.error(
            request,
            f'❌ Error rejecting profile: {str(e)}'
        )

    return redirect('admin_profiles')


@login_required
@user_passes_test(is_admin)
def admin_users(request):
    try:
        users = User.objects.all().order_by('-date_joined')
        return render(request, 'admin_panel/users.html', {
            'users': users
        })
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('admin_dashboard')


@login_required
@user_passes_test(is_admin)
def approve_all_pending(request):
    try:
        pending = Profile.objects.filter(is_approved=False)
        count = pending.count()

        for profile in pending:
            profile.is_approved = True
            profile.save()

            # Notify each user
            try:
                Notification.objects.create(
                    user=profile.user,
                    notification_type='profile_approved',
                    title='🎉 Profile Approved!',
                    message='Your profile is now live.',
                    link='/profiles/me/'
                )
            except Exception:
                pass

        messages.success(
            request,
            f'✅ {count} profiles approved!'
        )
    except Exception as e:
        messages.error(
            request,
            f'❌ Error: {str(e)}'
        )

    return redirect('admin_profiles')