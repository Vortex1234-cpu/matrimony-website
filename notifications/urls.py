from django.urls import path
from . import views

urlpatterns = [
    path(
        "mark-all-read/",
        views.mark_all_read,
        name="mark_all_read"
    ),

    path(
        "mark-read/<int:notification_id>/",
        views.mark_read,
        name="mark_read"
    ),

    path(
        "save-fcm-token/",
        views.save_fcm_token,
        name="save_fcm_token"
    ),
]