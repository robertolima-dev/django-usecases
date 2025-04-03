from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from apps.book.models import Book


@receiver(post_save, sender=Book)
def create_book(sender, instance, created, **kwargs):
    if created:
        print(instance)


@receiver(pre_delete, sender=Book)
def delete_book(sender, instance, **kwargs):
    print(instance.id)
