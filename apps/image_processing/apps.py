from django.apps import AppConfig


class ImageProcessingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.image_processing"

    # def ready(self):
    #     import apps.image_processing.signals  # noqa