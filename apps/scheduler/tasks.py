from celery import shared_task
from django.utils.timezone import localdate

from apps.throttle.models import UserQuota


@shared_task(name='throttle.reset_user_quotas')
def reset_user_quotas():
    today = localdate()
    restarted = 0

    for quota in UserQuota.objects.all():
        if quota.reset_date != today:
            quota.used = 0
            quota.reset_date = today
            quota.save()
            restarted += 1
            print(f"[Celery] Resetado: {quota.user} - {quota.action}")

    if restarted == 0:
        print("[Celery] Nenhuma cota foi resetada. Já estavam atualizadas.")
    else:
        print(f"[Celery] Total de cotas resetadas: {restarted}")
