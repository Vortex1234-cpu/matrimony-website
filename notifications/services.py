import requests
import json
from .models import DeviceToken


def send_push_notification(user, title, body, data=None):
    """
    Send a push notification to all devices of a specific user.
    
    Usage:
        from notifications.services import send_push_notification
        send_push_notification(user, "New Match!", "Someone liked your profile.")
    """
    tokens = DeviceToken.objects.filter(
        user=user,
        token__isnull=False
    ).values_list("token", flat=True)

    if not tokens:
        print(f"No device tokens found for user: {user.username}")
        return False

    results = []
    for token in tokens:
        result = _send_to_token(str(token), title, body, data or {})
        results.append(result)

    return all(results)


def send_push_to_all(title, body, data=None):
    """
    Send a push notification to ALL users with a registered token.
    Use sparingly — e.g. for announcements.
    """
    tokens = DeviceToken.objects.filter(
        user__isnull=False,
        token__isnull=False
    ).values_list("token", flat=True)

    results = []
    for token in tokens:
        result = _send_to_token(str(token), title, body, data or {})
        results.append(result)

    return results


def _send_to_token(token, title, body, data=None):
    """
    Internal: send FCM notification to a single device token
    using the FCM v1 HTTP API with a service account.
    """
    import google.auth
    import google.auth.transport.requests
    from google.oauth2 import service_account
    from django.conf import settings

    try:
        # Load service account credentials from your firebase_key.json
        credentials = service_account.Credentials.from_service_account_file(
            settings.FIREBASE_KEY_PATH,
            scopes=["https://www.googleapis.com/auth/firebase.messaging"]
        )

        # Refresh to get a valid access token
        auth_request = google.auth.transport.requests.Request()
        credentials.refresh(auth_request)
        access_token = credentials.token

        # Build the FCM v1 API URL
        project_id = credentials.project_id
        url = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"

        payload = {
            "message": {
                "token": token,
                "notification": {
                    "title": title,
                    "body": body
                },
                "data": {k: str(v) for k, v in (data or {}).items()},
                "android": {
                    "priority": "high"
                }
            }
        }

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            data=json.dumps(payload),
            timeout=10
        )

        if response.status_code == 200:
            print(f"✅ Notification sent to token: {token[:20]}...")
            return True
        else:
            print(f"❌ FCM error {response.status_code}: {response.text}")
            # If token is invalid/expired, delete it from DB
            if response.status_code == 404 or "UNREGISTERED" in response.text:
                DeviceToken.objects.filter(token=token).delete()
                print(f"🗑️ Deleted invalid token: {token[:20]}...")
            return False

    except Exception as e:
        print(f"❌ Exception sending to {token[:20]}: {e}")
        return False