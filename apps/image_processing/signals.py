from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import UploadedImage
from .tasks import create_thumbnail

# from common.sqs_sync import SqSManager


@receiver(post_save, sender=UploadedImage)
def generate_thumbnail(sender, instance, created, **kwargs):
    if created and instance.original_image:
        create_thumbnail.delay(instance.id)

        msg = {
            "apps": [{
                "endpoint": "{0}/api/v1/image-processing-sync".format(
                    settings.URL_BASE
                ),
                "key": settings.APP_KEY
            }],
            "data": {
                "obj_type": "image_processing",
                "obj_data": {
                    "image_id": instance.id
                },
                "obj_cmd": "put"
            },
            "timestamp": timezone.now().timestamp()
        }

        print(msg)

        # try:
        #     SqSManager.send(msg=msg)
        # except Exception as e:
        #     print(str(e))
