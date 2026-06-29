from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Notification
from .services import send_push_notification


@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):

    if not created:
        return

    send_push_notification(
        user=instance.user,
        title=instance.title,
        body=instance.message,
        data={
            "type": instance.notification_type,
            "link": instance.link or ""
        }
    )