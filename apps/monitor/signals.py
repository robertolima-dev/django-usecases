from celery import current_app
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_results.models import TaskResult


@receiver(post_save, sender=TaskResult)
def fill_task_name_if_missing(sender, instance, created, **kwargs):
    if created and not instance.task_name and instance.task_id:
        task = current_app.tasks.get(instance.task_id)
        if not task:
            for task_name, task_obj in current_app.tasks.items():
                if getattr(task_obj, 'request', None) and task_obj.request.id == instance.task_id:  # noqa: E501
                    instance.task_name = task_name
                    instance.save(update_fields=['task_name'])
                    break
