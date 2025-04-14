import os
import time
from io import BytesIO

from celery import shared_task
from django.core.files.base import ContentFile
from django.utils.text import slugify
from PIL import Image

from common.decorators.logging import log_task_execution

from .models import UploadedImage


@shared_task(name='image_processing.create_thumbnail')
@log_task_execution
def create_thumbnail(image_id):
    try:
        image_instance = UploadedImage.objects.get(id=image_id) # noqa501
        print(f"Iniciando processamento da imagem: {image_instance.original_image.name}") # noqa501
        time.sleep(1)

        original_path = image_instance.original_image.path
        image = Image.open(original_path).convert("RGB")
        base_name, _ = os.path.splitext(os.path.basename(original_path)) # noqa501
        base_slug = slugify(base_name)

        output_format = image_instance.output_format or 'JPEG'
        ext = 'webp' if output_format == 'WEBP' else 'jpg'

        sizes = {
            'thumbnail': (150, 150),
            'medium': (600, 600),
            'large': (1200, 1200),
        }

        for label, size in sizes.items():
            img_copy = image.copy()
            img_copy.thumbnail(size)

            buffer = BytesIO()
            img_copy.save(buffer, format=output_format, quality=85) # noqa501
            image_field = ContentFile(buffer.getvalue())
            filename = f"{label}_{base_slug}.{ext}"

            setattr(image_instance, label, image_field)
            getattr(image_instance, label).save(filename, image_field, save=False) # noqa501

        image_instance.save()
        print(f"✅ Imagens geradas para {image_instance.original_image.name}") # noqa501

    except Exception as e:
        print(f"❌ Erro ao gerar imagens: {str(e)}")
