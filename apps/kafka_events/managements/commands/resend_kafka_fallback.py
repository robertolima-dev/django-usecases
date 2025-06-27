
import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from kafka_events.fallbacks.kafka_fallback import FALLBACK_DIR
from kafka_events.utils.resilient_kafka_producer import safe_send_kafka_event


class Command(BaseCommand):
    help = "Reenvia eventos salvos no fallback local para o Kafka"

    def handle(self, *args, **kwargs):
        fallback_file = FALLBACK_DIR / f"{settings.KAFKA_COURSE_TOPIC}.log"

        if not fallback_file.exists():
            self.stdout.write(self.style.WARNING("⚠️ Nenhum fallback encontrado."))  # noqa: E501
            return

        with open(fallback_file, "r") as f:
            lines = f.readlines()

        if not lines:
            self.stdout.write(self.style.WARNING("📂 Fallback está vazio."))
            return

        self.stdout.write(self.style.NOTICE(f"🔄 Reenviando {len(lines)} eventos..."))  # noqa: E501

        sent = 0
        for line in lines:
            try:
                data = json.loads(line)
                event = data["event"]
                safe_send_kafka_event(settings.KAFKA_COURSE_TOPIC, event)
                sent += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Erro ao reenviar evento: {e}"))  # noqa: E501

        # Limpa o arquivo após sucesso
        Path(fallback_file).unlink()
        self.stdout.write(self.style.SUCCESS(f"✅ {sent} eventos reenviados com sucesso."))  # noqa: E501
