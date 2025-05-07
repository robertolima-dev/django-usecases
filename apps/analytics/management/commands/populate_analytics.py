from django.core.management.base import BaseCommand
from faker import Faker

from apps.analytics.mongo_client import db

fake = Faker()


class Command(BaseCommand):
    help = "Popula eventos de log no MongoDB"

    def handle(self, *args, **kwargs):
        for _ in range(1000):
            event = {
                "event_type": fake.random_element(["login", "logout", "purchase", "error"]), # noqa501
                "description": fake.sentence(),
                "timestamp": fake.date_time().isoformat()
            }
            db.event_logs.insert_one(event)
        self.stdout.write(self.style.SUCCESS("✅ 1000 eventos criados no MongoDB")) # noqa501
