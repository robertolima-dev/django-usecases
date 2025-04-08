from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UploadedImage

# from .tasks import create_thumbnail


@receiver(post_save, sender=UploadedImage)
def generate_thumbnail(sender, instance, created, **kwargs):
    print(instance)
    # print(instance.original_image)
    # if instance.original_image:
    #     create_thumbnail.delay(instance.id)
