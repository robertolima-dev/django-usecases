from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from apps.book.models import Book
from apps.kafka_events.producers.book_producer import send_book_created_event
from apps.mailer.tasks import send_mass_email


@receiver(post_save, sender=Book)
def book_created_email(sender, instance, created, **kwargs):
    if created:
        subject = f"Novo livro disponível: {instance.title}"
        content = f"Confira nosso novo livro: {instance.title}"
        send_book_created_event(instance)
        send_mass_email.delay(subject, content)


@receiver(pre_delete, sender=Book)
def delete_book(sender, instance, **kwargs):
    print(instance.id)
