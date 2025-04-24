from django.conf import settings
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.course.documents import CourseDocument
from apps.mailer.tasks import send_mass_email

from .models import Course  # Ou Book

USE_ELASTIC = settings.PROJECT_ENV == "local"


@receiver(post_save, sender=Course)
def course_created_email(sender, instance, created, **kwargs):
    if created:
        subject = f"Novo curso disponível: {instance.title}"
        content = f"Confira nosso novo curso: {instance.title}"
        send_mass_email.delay(subject, content)


if USE_ELASTIC:
    @receiver(post_save, sender=Course)
    def index_course(sender, instance, **kwargs):
        CourseDocument.update_or_create_document(instance)

    @receiver(post_delete, sender=Course)
    def delete_course(sender, instance, **kwargs):
        CourseDocument.delete_document(instance)
