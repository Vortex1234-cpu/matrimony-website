from firebase_admin import messaging


def send_push(token, title, body, data=None):
    """
    Send a push notification to a single Android device.
    """

    if data is None:
        data = {}

    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            token=token,
        )

        response = messaging.send(message)

        print("✅ Firebase Response:", response)

        return True

    except Exception as e:
        print("❌ Firebase Error:", e)
        return False