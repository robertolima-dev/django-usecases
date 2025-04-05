from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.throttle.models import UserQuota

User = get_user_model()

DEFAULT_ACTIONS = {
    "upload": 5,
    "report": 3,
    "api_access": 100,
}


class Command(BaseCommand):
    help = "Cria cotas padrão para todos os usuários existentes"

    def handle(self, *args, **options):
        total_created = 0
        for user in User.objects.all():
            for action, limit in DEFAULT_ACTIONS.items():
                quota, created = UserQuota.objects.get_or_create(
                    user=user,
                    action=action,
                    defaults={
                        "limit": limit,
                        "used": 0,
                        "reset_date": date.today()
                    }
                )
                if created:
                    total_created += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Cota criada: {user} - {action} ({limit})"
                        )
                    )

        if total_created == 0:
            self.stdout.write(self.style.WARNING("Nenhuma cota nova criada."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Total: {total_created} novas cotas criadas.")) # noqa501
