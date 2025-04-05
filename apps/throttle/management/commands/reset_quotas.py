from datetime import date

from django.core.management.base import BaseCommand

from apps.throttle.models import UserQuota


class Command(BaseCommand):
    help = "Reseta as cotas diárias dos usuários se a data de reset for diferente de hoje." # noqa501

    def handle(self, *args, **kwargs):
        today = date.today()
        restarted = 0

        for quota in UserQuota.objects.all():
            if quota.reset_date != today:
                quota.used = 0
                quota.reset_date = today
                quota.save()
                restarted += 1
                self.stdout.write(self.style.SUCCESS(f"Resetado: {quota.user} - {quota.action}")) # noqa501

        if restarted == 0:
            self.stdout.write(self.style.WARNING("Nenhuma cota foi resetada. Já estavam atualizadas.")) # noqa501
        else:
            self.stdout.write(self.style.SUCCESS(f"Total de cotas resetadas: {restarted}")) # noqa501
