from django.core.mail import send_mail
from django.conf import settings


def send_interest_notification(sender_profile, receiver):
    """
    Send an email to the receiver when someone sends them an interest.
    sender_profile: Profile instance of the person who sent interest
    receiver: User instance of the person receiving interest
    """
    subject = "Someone is interested in your profile!"

    sender_name = sender_profile.user.get_full_name() or sender_profile.user.username

    message = f"""
Hi {receiver.get_full_name() or receiver.username},

Great news! {sender_name} has shown interest in your profile on Matrimony App.

Log in to your account to view their profile and respond to their interest.

Best regards,
The Matrimony App Team
"""

    html_message = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
    <div style="background-color: #f8f0f5; padding: 30px; border-radius: 10px;">
        <h2 style="color: #8B1A4A;">💌 New Interest Received!</h2>
        <p>Hi <strong>{receiver.get_full_name() or receiver.username}</strong>,</p>
        <p>Great news! <strong>{sender_name}</strong> has shown interest in your profile on <strong>Matrimony App</strong>.</p>
        <p>Log in to your account to view their profile and respond to their interest.</p>
        <br>
        <a href="http://127.0.0.1:8000/matches/"
           style="background-color: #8B1A4A; color: white; padding: 12px 25px;
                  text-decoration: none; border-radius: 5px; display: inline-block;">
            View Profile
        </a>
        <br><br>
        <p style="color: #888; font-size: 13px;">Best regards,<br>The Matrimony App Team</p>
    </div>
</body>
</html>
"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[receiver.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"[Email Error] Failed to send interest notification: {e}")
        return False