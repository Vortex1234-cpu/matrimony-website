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
        # Debug: log exactly what we receive
        raw_body = request.body
        content_type = request.META.get("CONTENT_TYPE", "")
        print("=" * 60)
        print("CONTENT-TYPE:", content_type)
        print("RAW BODY:", raw_body)
        print("POST DATA:", request.POST)
        print("=" * 60)

        # Try JSON body first, fall back to form POST
        token = None
        if raw_body:
            try:
                data = json.loads(raw_body)
                token = data.get("token") or data.get("fcm_token")
                print("PARSED JSON TOKEN:", token)
            except json.JSONDecodeError:
                # Not JSON — try form field
                token = request.POST.get("token") or request.POST.get("fcm_token")
                print("FORM TOKEN:", token)
        else:
            token = request.POST.get("token") or request.POST.get("fcm_token")
            print("FORM TOKEN (empty body):", token)

        if not token:
            print("NO TOKEN FOUND — returning 400")
            return JsonResponse(
                {"status": "error", "message": "Token is required"},
                status=400
            )

        DeviceToken.objects.update_or_create(
            token=token,
            defaults={
                "user": request.user if request.user.is_authenticated else None
            }
        )

        print("TOKEN SAVED:", token[:20], "user:", request.user if request.user.is_authenticated else None)

        return JsonResponse(
            {
                "status": "success",
                "message": "FCM token saved successfully"
            }
        )

    except Exception as e:
        print("EXCEPTION in save_fcm_token:", str(e))
        return JsonResponse(
            {
                "status": "error",
                "message": str(e)
            },
            status=500
        )