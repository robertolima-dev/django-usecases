from datetime import date

from django.core.exceptions import ValidationError

from .models import UserQuota


def check_and_increment_quota(user, action):
    """
    Verifica se o usuário ainda tem cota disponível para a ação e incrementa o uso.
    Lança PermissionDenied se ultrapassado.
    """ # noqa501
    quota, _ = UserQuota.objects.get_or_create(
        user=user,
        action=action,
        defaults={
            "limit": 10,
            "used": 0,
            "reset_date": date.today(),
        }
    )

    if quota.reset_date != date.today():
        quota.used = 0
        quota.reset_date = date.today()
        quota.save()

    if quota.used >= quota.limit:
        raise ValidationError("Cota excedida para {0}. Limite diário atingido.".format(action)) # noqa501

    quota.used += 1
    quota.save()
