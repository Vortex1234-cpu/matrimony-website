from .models import DeviceToken
from .firebase import send_push


def send_push_notification(user, title, body, data=None):
    """
    Send notification to all registered Android devices of a user.
    """

    devices = DeviceToken.objects.filter(user=user)

    success = 0

    for device in devices:

        if send_push(
            token=device.token,
            title=title,
            body=body,
            data=data
        ):
            success += 1

    return success