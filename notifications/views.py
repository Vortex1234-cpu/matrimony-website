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
        raw_body = request.body
        token = None

        if raw_body:
            try:
                data = json.loads(raw_body)
                token = data.get("token") or data.get("fcm_token")
            except json.JSONDecodeError:
                token = request.POST.get("token") or request.POST.get("fcm_token")
        else:
            token = request.POST.get("token") or request.POST.get("fcm_token")

        if not token:
            return JsonResponse(
                {"status": "error", "message": "Token is required"},
                status=400
            )

        if request.user.is_authenticated:
            # Authenticated — always link/update this token to the logged-in user
            DeviceToken.objects.update_or_create(
                token=token,
                defaults={"user": request.user}
            )
            print("TOKEN SAVED with user:", request.user.username)

        else:
            # Not authenticated — only CREATE a new row if this token
            # doesn't exist yet. Never overwrite an existing user link with None.
            obj, created = DeviceToken.objects.get_or_create(
                token=token,
                defaults={"user": None}
            )
            if not created and obj.user is not None:
                print("TOKEN EXISTS with user:", obj.user.username, "— not overwriting")
            else:
                print("TOKEN SAVED with user=None (new anonymous token)")

        return JsonResponse({
            "status": "success",
            "message": "FCM token saved successfully"
        })

    except Exception as e:
        print("EXCEPTION in save_fcm_token:", str(e))
        return JsonResponse(
            {"status": "error", "message": str(e)},
            status=500
        )