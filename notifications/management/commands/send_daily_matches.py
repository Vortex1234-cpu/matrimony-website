from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from datetime import date

User = get_user_model()


class Command(BaseCommand):
    help = 'Send daily match suggestions to all active users'

    def handle(self, *args, **kwargs):
        from profiles.models import Profile
        from notifications.models import Notification

        self.stdout.write('Starting daily match suggestions...')

        # Get all users with complete, approved profiles
        users = User.objects.filter(
            is_profile_complete=True,
            is_active=True,
        )

        sent_count = 0
        skipped_count = 0

        for user in users:
            try:
                # Get the user's own profile
                if not hasattr(user, 'profile'):
                    skipped_count += 1
                    continue

                user_profile = user.profile

                if not user_profile.is_approved:
                    skipped_count += 1
                    continue

                # Determine opposite gender to suggest
                opposite_gender = (
                    'female' if user.gender == 'male' else 'male'
                )

                # Find matching profiles — same religion, opposite gender,
                # approved, not the user themselves
                matches = Profile.objects.filter(
                    is_approved=True,
                    gender=opposite_gender,
                ).exclude(
                    user=user
                ).exclude(
                    user__in=self._already_interacted(user)
                )

                # Apply religion filter if set
                if user_profile.religion:
                    matches = matches.filter(
                        religion=user_profile.religion
                    )

                # Apply partner preference age range if set
                try:
                    pref = user.preference
                    today = date.today()

                    # Convert age range to birth year range
                    min_birth_year = today.year - pref.max_age
                    max_birth_year = today.year - pref.min_age

                    matches = matches.filter(
                        date_of_birth__year__gte=min_birth_year,
                        date_of_birth__year__lte=max_birth_year,
                    )
                except Exception:
                    pass  # No preference set, skip filter

                # Pick top 3 fresh matches
                matches = matches.order_by('-created_at')[:3]

                if not matches:
                    skipped_count += 1
                    continue

                match_names = ', '.join(
                    [m.full_name for m in matches]
                )
                match_count = len(matches)

                # ── In-app notification ──────────────────────────
                Notification.objects.create(
                    user=user,
                    notification_type='daily_matches',
                    title=f'💑 {match_count} New Match Suggestion{"s" if match_count > 1 else ""} Today!',
                    message=(
                        f'We found {match_count} profile{"s" if match_count > 1 else ""} '
                        f'that match your preferences: {match_names}. '
                        f'Visit Search to connect with them.'
                    ),
                    link='/search/',
                )

                # ── Email ────────────────────────────────────────
                if user.email:
                    self._send_email(user, matches)

                sent_count += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error for user {user.phone}: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Done! Sent: {sent_count}, Skipped: {skipped_count}'
            )
        )

    def _already_interacted(self, user):
        """Return user IDs this user has already sent/received interest with."""
        from matches.models import Interest
        sent = Interest.objects.filter(
            sender=user
        ).values_list('receiver_id', flat=True)
        received = Interest.objects.filter(
            receiver=user
        ).values_list('sender_id', flat=True)
        return list(set(list(sent) + list(received)))

    def _send_email(self, user, matches):
        profile_lines = ''
        for m in matches:
            profile_lines += (
                f'• {m.full_name} — {m.age()} yrs, '
                f'{m.city}, {m.district} | '
                f'{m.religion.capitalize()}'
                f'{", " + m.caste if m.caste else ""}\n'
            )

        site_url = getattr(settings, 'SITE_URL', 'https://rajapalayammatrimony.com')

        subject = '💑 Your Daily Match Suggestions — Rajapalayam Matrimony'
        message = f"""Hello {user.first_name or user.phone},

Good morning! ☀️ Here are today's match suggestions for you:

{profile_lines}
👉 View & connect with them here: {site_url}/search/

These profiles match your preferences. Don't wait — send them an interest today!

— Rajapalayam Matrimony Team
📧 rajapalayammatrimony.com@gmail.com
📞 +91 75 023 023 33

To stop receiving these emails, update your preferences in your account settings.
"""
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )