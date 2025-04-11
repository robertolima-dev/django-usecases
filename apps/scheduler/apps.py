from django.apps import AppConfig
from django.db import connection


class SchedulerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.scheduler"

    def ready(self):
        import json

        from django.db.utils import OperationalError, ProgrammingError
        from django.utils.timezone import now
        from django_celery_beat.models import CrontabSchedule, PeriodicTask

        try:
            if 'django_celery_beat_crontabschedule' in connection.introspection.table_names(): # noqa501

                task_name = "apps.scheduler.tasks.reset_user_quotas"
                schedule, _ = CrontabSchedule.objects.update_or_create(
                    minute="0",
                    hour="0",
                    day_of_week="*",
                    day_of_month="*",
                    month_of_year="*",
                    timezone="UTC"
                )

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

    # def ready(self):
    #     import json

    #     from django.utils.timezone import now
    #     from django_celery_beat.models import CrontabSchedule, PeriodicTask

    #     task_name = "apps.scheduler.tasks.reset_user_quotas"
    #     schedule, _ = CrontabSchedule.objects.update_or_create(
    #         minute='0',
    #         hour='0',
    #         day_of_week='*',
    #         day_of_month='*',
    #         month_of_year='*',
    #         timezone='UTC',
    #     )

    #     PeriodicTask.objects.get_or_create(
    #         name='Reset User Quotas',
    #         defaults={
    #             'task': task_name,
    #             'crontab': schedule,
    #             'start_time': now(),
    #             'enabled': True,
    #             'kwargs': json.dumps({}),
    #         }
    #     )
