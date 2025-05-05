import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.knowledge.models import KnowledgeStudy, KnowledgeTopic

User = get_user_model()


class Command(BaseCommand):
    help = "Popula estudos simulados dos tópicos por usuários fictícios"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        topics = KnowledgeTopic.objects.all()

        if not users.exists():
            self.stdout.write(self.style.WARNING("⚠️ Nenhum usuário encontrado. Crie usuários primeiro.")) # noqa501
            return

        count = 0
        for topic in topics:
            sample_users = random.sample(list(users), min(2, users.count()))
            for user in sample_users:
                study, created = KnowledgeStudy.objects.get_or_create(
                    topic=topic,
                    user=user,
                    defaults={"notes": f"Estudo automático sobre {topic.title}."} # noqa501
                )
                if created:
                    count += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {count} registros de estudo criados.")) # noqa501
