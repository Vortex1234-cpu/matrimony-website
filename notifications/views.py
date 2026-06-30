from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from .models import Notification, DeviceToken
import json

User = get_user_model()


@login_required
def mark_all_read(request):
    Notification.objects.filter(
        user=request.user,
        is_read=False
    ).update(is_read=True)
    return redirect("dashboard")


@login_required
def mark_read(request, notification_id):
    try:
        notification = Notification.objects.get(
            id=notification_id,
            user=request.user
        )
        notification.is_read = True
        notification.save()
    except Notification.DoesNotExist:
        pass

    return redirect("dashboard")


@csrf_exempt
def save_fcm_token(request):

    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "POST request required"},
            status=400
        )

    try:
        data = json.loads(request.body)
        token = data.get("token")

        if not token:
            return JsonResponse(
                {"status": "error", "message": "Token is required"},
                status=400
            )

        # Always key off the token, not the user. A token uniquely
        # identifies one device/app-install; a user can have several
        # devices, so looking up by user would overwrite a different
        # device's row every time that same user logs in elsewhere.
        DeviceToken.objects.update_or_create(
            token=token,
            defaults={
                "user": request.user if request.user.is_authenticated else None
            }
        )

        return JsonResponse(
            {
                "status": "success",
                "message": "FCM token saved successfully"
            }
        )

    except Exception as e:
        return JsonResponse(
            {
                "status": "error",
                "message": str(e)
            },
            status=500
        )