import json

from django.apps import AppConfig
from django.db import connection
from django.db.utils import OperationalError, ProgrammingError
from django.utils.timezone import now


class SchedulerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.scheduler"

    def ready(self):
        try:
            if 'django_celery_beat_crontabschedule' in connection.introspection.table_names():   # noqa: E501
                from django_celery_beat.models import CrontabSchedule, PeriodicTask

                task_name = "apps.scheduler.tasks.reset_user_quotas"

                # Tenta pegar o primeiro schedule existente
                schedule = CrontabSchedule.objects.filter(
                    minute="0",
                    hour="0",
                    day_of_week="*",
                    day_of_month="*",
                    month_of_year="*",
                    timezone="UTC"
                ).first()

                # Cria se não existir
                if not schedule:
                    schedule = CrontabSchedule.objects.create(
                        minute="0",
                        hour="0",
                        day_of_week="*",
                        day_of_month="*",
                        month_of_year="*",
                        timezone="UTC"
                    )

                # Cria a tarefa periódica se ainda não existir
                PeriodicTask.objects.get_or_create(
                    name='Reset User Quotas',
                    defaults={
                        'task': task_name,
                        'crontab': schedule,
                        'start_time': now(),
                        'enabled': True,
                        'kwargs': json.dumps({}),
                    }
                )

        except (OperationalError, ProgrammingError):
            pass
