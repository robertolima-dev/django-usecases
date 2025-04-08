from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.mailer.tasks import send_mass_email

from .models import Course  # Ou Book


@receiver(post_save, sender=Course)
def course_created_email(sender, instance, created, **kwargs):
    if created:
        subject = f"Novo curso disponível: {instance.title}"
        content = f"Confira nosso novo curso: {instance.title}"
        send_mass_email.delay(subject, content)
