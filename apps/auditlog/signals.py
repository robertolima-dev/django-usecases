import json

from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connection
from django.db.models.signals import post_delete, post_save
from django.db.utils import OperationalError, ProgrammingError
from django.dispatch import receiver
from django.forms.models import model_to_dict
from django.utils.timezone import now

from .models import AuditLog

User = get_user_model()


def get_user_from_instance(instance):
    for attr in ["user", "created_by", "owner", "author", "instructor", "sender"]:  # noqa: E501
        if hasattr(instance, attr):
            user = getattr(instance, attr)
            if isinstance(user, User) and User.objects.filter(pk=user.pk).exists():  # noqa: E501
                return user
    return None


@receiver(post_save)
def log_save(sender, instance, created, **kwargs):
    print(f'log_save => {instance}')
    if sender.__name__ in ["AuditLog", "PeriodicTasks", "PeriodicTask", "TaskResult"]:  # noqa: E501
        return  # Evita loop

    user = get_user_from_instance(instance)
    action = "create" if created else "update"

    changes = model_to_dict(instance)

    try:
        changes_json = json.dumps(changes, cls=DjangoJSONEncoder)
    except Exception:
        changes_json = json.dumps({k: str(v) for k, v in changes.items()})

    try:
        if 'auditlog_auditlog' in connection.introspection.table_names():
            AuditLog.objects.create(
                user=user if isinstance(user, AuditLog._meta.get_field('user').remote_field.model) else None,  # noqa: E501
                action=action,
                model=sender.__name__,
                object_id=str(instance.pk),
                object_repr=str(instance),
                changes=changes_json,
                timestamp=now()
            )
    except (OperationalError, ProgrammingError):
        pass


@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender in [AuditLog, User]:  # ← ignora User e AuditLog
        return

    user = get_user_from_instance(instance)
    user = user if isinstance(user, User) and User.objects.filter(pk=user.pk).exists() else None  # noqa: E501

    if user:

        try:
            if 'auditlog_auditlog' in connection.introspection.table_names():
                AuditLog.objects.create(
                    user=user if isinstance(user, User) else None,
                    action="delete",
                    model=sender.__name__,
                    object_id=str(instance.pk),
                    object_repr=str(instance),
                    changes=None,
                    timestamp=now()
                )
        except (OperationalError, ProgrammingError):
            pass
