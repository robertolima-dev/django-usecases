from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from django.contrib.auth.models import User

from apps.notifications.models import Notification


@shared_task(name='course.notification_users_course')
def notification_users_course(notification_id):

    try:

        notification = Notification.objects.filter(
            id=notification_id
        ).first()

        channel_layer = get_channel_layer()
        for user in User.objects.all():
            async_to_sync(channel_layer.group_send)(
                f"user_{user.id}",
                {
                    "type": "send_notification",
                    "title": notification.title,
                    "message": notification.message,
                    "created_at": str(notification.created_at),
                    "obj_code": notification.obj_code,
                    "obj_id": notification.obj_id,
                }
            )

    except Exception as e:
        print(str(e))
        raise e
