import os
import time
from io import BytesIO

from celery import shared_task
from django.core.files.base import ContentFile
from django.utils.text import slugify
# from django.core.files.storage import default_storage
from PIL import Image

from .models import UploadedImage


@shared_task
def create_thumbnail(image_id):

    try:
        image_instance = UploadedImage.objects.get(id=image_id)

        print(f"Iniciando processamento da imagem: {image_instance.original_image.name}") # noqa501
        time.sleep(1)

        original_path = image_instance.original_image.path
        thumb_size = (200, 200)

        with Image.open(original_path) as img:
            img.thumbnail(thumb_size)
            thumb_io = BytesIO()
            img.save(thumb_io, img.format, quality=85)

            original_filename = image_instance.original_image.name.split('/')[-1] # noqa501
            name, ext = os.path.splitext(original_filename)
            thumbnail_name = f"thumb_{slugify(name)}{ext}"
            print(thumbnail_name)

            image_instance.thumbnail.save(thumbnail_name, ContentFile(thumb_io.getvalue())) # noqa501

        image_instance.save()
        print(f"Thumbnail criado: {image_instance.thumbnail.name}")

    except Exception as e:
        print(str(e))
