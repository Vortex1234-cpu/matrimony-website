import logging
import random
import string

logger = logging.getLogger(__name__)
from django.conf import settings
SITE_URL = getattr(settings, 'SITE_URL', 'https://rajapalayammatrimony.com')

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def send_otp_email(user, otp):
    try:
        if not user.email:
            logger.warning(f'No email for {user.username}')
            return False

        from django.core.mail import EmailMultiAlternatives
        from django.conf import settings

        if not settings.EMAIL_HOST_USER:
            logger.error('EMAIL_HOST_USER not configured')
            return False

        if not settings.EMAIL_HOST_PASSWORD:
            logger.error('EMAIL_HOST_PASSWORD not configured')
            return False

        subject = f'Your Rajapalayam Matrimony OTP: {otp}'

        text_content = (
            f'Hello {user.first_name},\n\n'
            f'Your OTP is: {otp}\n\n'
            f'Valid for 10 minutes.\n'
            f'Do not share with anyone.\n\n'
            f'Rajapalayam Matrimony Team'
        )

        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
</head>
<body style="font-family:Arial,sans-serif;background:#fff8f0;margin:0;padding:20px;">
<div style="max-width:480px;margin:0 auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(139,0,0,0.1);">

    <div style="background:linear-gradient(135deg,#5c0000,#8B0000);padding:30px;text-align:center;">
        <h1 style="color:#d4af37;margin:0;font-size:1.6rem;font-family:Georgia,serif;">
            💍 Rajapalayam Matrimony
        </h1>
        <p style="color:rgba(255,255,255,0.8);margin:8px 0 0;font-size:0.9rem;">
            Email Verification
        </p>
    </div>

    <div style="padding:35px;text-align:center;">
        <p style="color:#555;font-size:1rem;margin-bottom:8px;">
            Hello <strong>{user.first_name}</strong>,
        </p>
        <p style="color:#555;margin-bottom:20px;">
            Your verification OTP is:
        </p>
        <div style="background:linear-gradient(135deg,#fff3cd,#ffeaa7);border:2px dashed #d4af37;border-radius:16px;padding:28px;margin:0 0 20px;">
            <div style="font-size:3.2rem;font-weight:900;color:#8B0000;letter-spacing:14px;">
                {otp}
            </div>
            <p style="color:#856404;margin:12px 0 0;font-size:0.85rem;">
                ⏰ Valid for 10 minutes only
            </p>
        </div>
        <p style="color:#888;font-size:0.82rem;line-height:1.6;">
            Do not share this OTP with anyone.<br>
            Rajapalayam Matrimony will never ask for your OTP.
        </p>
    </div>

    <div style="background:#f8f8f8;padding:16px;text-align:center;color:#888;font-size:0.78rem;">
        © 2024 Rajapalayam Matrimony | Rajapalayam, Tamil Nadu
    </div>

</div>
</body>
</html>'''

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)

        logger.info(f'OTP sent to {user.email}')
        print(f'✅ OTP email sent to {user.email}')
        return True

    except Exception as e:
        logger.error(f'OTP email failed: {str(e)}')
        print(f'❌ OTP email error: {str(e)}')
        return False


def send_interest_received_email(receiver, sender):
    try:
        if not receiver.email:
            return False
        from django.core.mail import EmailMultiAlternatives
        from django.conf import settings
        if not settings.EMAIL_HOST_USER:
            return False

        subject = (
            f'💌 {sender.first_name} sent you an interest '
            f'- Rajapalayam Matrimony'
        )
        html_content = f'''<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;background:#fff8f0;margin:0;padding:20px;">
<div style="max-width:500px;margin:0 auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(139,0,0,0.1);">
    <div style="background:linear-gradient(135deg,#5c0000,#8B0000);padding:30px;text-align:center;">
        <h1 style="color:#d4af37;margin:0;font-family:Georgia,serif;">
            💍 Rajapalayam Matrimony
        </h1>
    </div>
    <div style="padding:30px;">
        <p style="color:#333;">Hello <strong>{receiver.first_name}</strong>,</p>
        <div style="background:#fff3cd;border-left:4px solid #d4af37;border-radius:8px;padding:16px;margin:16px 0;">
            <strong>💌 {sender.first_name}</strong> has sent you an interest request!
        </div>
        <p style="color:#555;font-size:0.9rem;line-height:1.7;">
            Login to Rajapalayam Matrimony to view their profile and respond to the interest.
        </p>
        <div style="text-align:center;margin-top:25px;">
            <a href="{SITE_URL}/matches/received/"
               style="background:linear-gradient(135deg,#8B0000,#c0392b);color:#fff;padding:14px 32px;border-radius:50px;text-decoration:none;font-weight:700;">
                View Interest →
            </a>
        </div>
    </div>
    <div style="background:#f8f8f8;padding:16px;text-align:center;color:#888;font-size:0.78rem;">
        © 2024 Rajapalayam Matrimony | Rajapalayam, Tamil Nadu
    </div>
</div>
</body>
</html>'''

        msg = EmailMultiAlternatives(
            subject=subject,
            body=f'{sender.first_name} sent you an interest on Rajapalayam Matrimony!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[receiver.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        return True
    except Exception as e:
        print(f'Interest email error: {e}')
        return False


def send_interest_accepted_email(sender, receiver):
    try:
        if not sender.email:
            return False
        from django.core.mail import EmailMultiAlternatives
        from django.conf import settings
        if not settings.EMAIL_HOST_USER:
            return False

        subject = (
            f'🎉 {receiver.first_name} accepted your interest '
            f'- Rajapalayam Matrimony'
        )
        html_content = f'''<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;background:#fff8f0;margin:0;padding:20px;">
<div style="max-width:500px;margin:0 auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(139,0,0,0.1);">
    <div style="background:linear-gradient(135deg,#27ae60,#2ecc71);padding:30px;text-align:center;">
        <h1 style="color:#fff;margin:0;font-family:Georgia,serif;">
            🎉 Interest Accepted!
        </h1>
    </div>
    <div style="padding:30px;">
        <p style="color:#333;">Hello <strong>{sender.first_name}</strong>,</p>
        <div style="background:#e8f5e9;border-left:4px solid #27ae60;border-radius:8px;padding:16px;">
            <strong>{receiver.first_name}</strong> has accepted your interest!
            You can now connect and start a conversation.
        </div>
        <div style="text-align:center;margin-top:25px;">
            <a href="{SITE_URL}/matches/mutual/"
               style="background:linear-gradient(135deg,#27ae60,#2ecc71);color:#fff;padding:14px 32px;border-radius:50px;text-decoration:none;font-weight:700;">
                View Match →
            </a>
        </div>
    </div>
    <div style="background:#f8f8f8;padding:16px;text-align:center;color:#888;font-size:0.78rem;">
        © 2024 Rajapalayam Matrimony | Rajapalayam, Tamil Nadu
    </div>
</div>
</body>
</html>'''

        msg = EmailMultiAlternatives(
            subject=subject,
            body=f'{receiver.first_name} accepted your interest on Rajapalayam Matrimony!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sender.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)
        return True
    except Exception as e:
        print(f'Accept email error: {e}')
        return False


def send_profile_approved_email(user):
    try:
        if not user.email:
            return False
        from django.core.mail import EmailMultiAlternatives
        from django.conf import settings
        if not settings.EMAIL_HOST_USER:
            return False

        subject = '🎉 Your Rajapalayam Matrimony Profile is Approved!'
        html_content = f'''<!DOCTYPE html>
<html>
<body style="font-family:Arial,sans-serif;background:#fff8f0;margin:0;padding:20px;">
<div style="max-width:500px;margin:0 auto;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(139,0,0,0.1);">
    <div style="background:linear-gradient(135deg,#5c0000,#8B0000);padding:30px;text-align:center;">
        <h1 style="color:#d4af37;margin:0;font-family:Georgia,serif;">
            💍 Rajapalayam Matrimony
        </h1>
    </div>
    <div style="padding:30px;">
        <p style="color:#333;">Hello <strong>{user.first_name}</strong>,</p>
        <div style="background:#e8f5e9;border-left:4px solid #27ae60;border-radius:8px;padding:16px;margin:16px 0;">
            <strong>🎉 Congratulations! Your profile is approved.</strong><br>
            <span style="color:#555;font-size:0.9rem;">
                Your profile is now live and visible to matches.
            </span>
        </div>
        <p style="color:#555;font-size:0.9rem;line-height:1.7;">
            Start browsing profiles and send interests to find your perfect match!
        </p>
        <div style="text-align:center;margin-top:25px;">
            <a href="{SITE_URL}/search/"
               style="background:linear-gradient(135deg,#8B0000,#c0392b);color:#fff;padding:14px 32px;border-radius:50px;text-decoration:none;font-weight:700;">
                Browse Matches →
            </a>
        </div>
    </div>
    <div style="background:#f8f8f8;padding:16px;text-align:center;color:#888;font-size:0.78rem;">
        © 2024 Rajapalayam Matrimony | Rajapalayam, Tamil Nadu
    </div>
</div>
</body>
</html>'''

        msg = EmailMultiAlternatives(
            subject=subject,
            body='Your profile has been approved on Rajapalayam Matrimony!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)
        return True
    except Exception as e:
        print(f'Approval email error: {e}')
        return False