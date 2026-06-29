from firebase_admin import messaging


def send_push(token, title, body, data=None):
    if data is None:
        data = {}

    print("=" * 60)
    print("Sending notification...")
    print("Token:", token)
    print("Title:", title)
    print("Body:", body)
    print("Data:", data)

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

        print("Firebase Response:", response)

        return True

    except Exception as e:
        print("Firebase Error:", repr(e))
        return False